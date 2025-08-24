import asyncio
import json
from pathlib import Path
from time import sleep

from rabbitmq_adapter.rabbitmq_adapter import RabbitMqAdapter
from settings import DEVICE_SLEEP_TIME, MAX_ATTEMPT, SLEEP_TIME
from tapo import ApiClient
from tapo_adapter.device import Device
from tenacity import retry, stop_after_attempt, wait_fixed
from yaspin import yaspin


class PlugP110(Device):
    """Specific implementation for the Tapo P110 smart plug."""

    # State is used to denote if the device is in usage based on the current power usage
    _state: bool = False
    _device = None

    def __init__(
        self,
        name: str,
        mac: str,
        client: ApiClient,
        rabbitmq: RabbitMqAdapter,
        ip: str = None,
    ):
        """
        :param name: Name of the device
        :param mac: MAC address of the device
        :param client: Tapo API client object
        :param ip: Static IP address of the device
        """
        super().__init__(mac, client, ip)
        self._name = name
        self._rabbitmq = rabbitmq
        state_file = Path(f"state-{mac.replace(':', '-')}.json")

        # Load state from file if exists
        if state_file.exists():
            try:
                with open(state_file, "r") as file:
                    data = json.load(file)
                    if "state" in data:
                        self._state = data["state"]
                        print(f"[{self._mac}] Restored state: {self._state}")
            except Exception as e:
                print(f"[{self._mac}] Failed to read state file: {e}")

    @retry(
        wait=wait_fixed(SLEEP_TIME), stop=stop_after_attempt(MAX_ATTEMPT), reraise=True
    )
    async def init(self):
        """Initialize the P110 device connection."""
        with yaspin(
            text=f"Trying to connect to P110 device with IP address `{self._ip}` ({self._mac})..."
        ):
            self._device = await self._client.p110(self._ip)

    async def get_state(self) -> bool:
        """
        Retrieve actual state from the P110 device.
        :return: True if device is turned on, otherwise False
        """
        if not self._device:
            await self.init()
        info = await self._device.get_device_info()
        return info.device_on

    async def polling(self):
        """
        Used for polling information from Tapo API about smart plug current power usage
        """
        while True:
            try:
                current_power_result = await self._device.get_current_power()
                current_state = current_power_result.current_power > 0
                print(f"{self._name} - {current_state}")
                if current_state != self._state:
                    await self._rabbitmq.amqp_handler(
                        {
                            "device": self._name,
                            "mac": self.mac,
                            "state": current_state,
                        }
                    )
                    self._state = current_state
                sleep(DEVICE_SLEEP_TIME)
            except Exception:
                # TODO Log here
                # TODO Update to distinguish between RabbitMQ error and Tapo error
                print(f"Polling error for {self._name}: {e}")

    def save_state(self):
        """Persist state to JSON file on service shutdown."""
        try:
            with open(Path(f"state-{self._mac.replace(':', '-')}.json"), "w") as file:
                json.dump({"state": self._state}, file)
                print(f"[{self._mac}] Saved state: {self._state}")
        except Exception as e:
            print(f"[{self._mac}] Failed to save state: {e}")
