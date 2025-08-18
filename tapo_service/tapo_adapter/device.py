from tapo import ApiClient
from tapo_adapter.device_interface import DeviceInterface
from util.network_util import NetworkUtil


class Device(DeviceInterface):
    """Concrete implementation of a smart device."""

    def __init__(self, mac: str, client: ApiClient, ip: str = None):
        self._client = client
        self._device = None  # Subclasses will set this
        self._mac = mac
        # If IP is empty, find it dynamically
        if ip is None:
            ip = NetworkUtil.get_ip_from_mac(mac)
            if ip is None:
                raise RuntimeError(
                    f"Failed to get an IP address for device with a MAC address {mac}."
                )
        self._ip = NetworkUtil.get_ip_from_mac(mac)

    async def turn_on(self):
        if self._device:
            info = await self._device.get_device_info()
            if not info.device_on:
                await self._device.on()
                self._state = True
                print(f"Device at {self._ip} turned ON")

    async def turn_off(self):
        if self._device:
            info = await self._device.get_device_info()
            if info.device_on:
                await self._device.off()
                self._state = False
                print(f"Device at {self._ip} turned OFF")
