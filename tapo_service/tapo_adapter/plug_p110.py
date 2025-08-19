import json
from pathlib import Path
from time import sleep

from rabbitmq_adapter.rabbitmq_adapter import RabbitMqAdapter
from settings import DEVICE_SLEEP_TIME
from tapo import ApiClient
from tapo_adapter.device import Device


class PlugP110(Device):
    """Specific implementation for the Tapo P110 smart plug."""

    # State is used to denote if the device is in usage based on the current power usage
    _state: bool = False

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

    async def init(self):
        """Initialize the P110 device connection."""
        self._device = await self._client.p110(self._ip)

    async def get_state(self) -> bool:
        """Retrieve actual state from the P110 device."""
        if not self._device:
            await self.init()
        info = await self._device.get_device_info()
        self._state = info.device_on
        return self._state

    async def pooling(self):
        """
        Used to Pool information from Tapo API about smart plug current power usage
        """
        while True:
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

    def save_state(self):
        """Persist state to JSON file on service shutdown."""
        try:
            with open(Path(f"state-{self._mac.replace(':', '-')}.json"), "w") as file:
                json.dump({"state": self._state}, file)
                print(f"[{self._mac}] Saved state: {self._state}")
        except Exception as e:
            print(f"[{self._mac}] Failed to save state: {e}")
