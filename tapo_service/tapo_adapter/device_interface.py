from abc import ABCMeta, abstractmethod


class DeviceInterface(metaclass=ABCMeta):
    """Abstract interface for a smart device."""

    @abstractmethod
    async def turn_on(self):
        """Turn the device on."""
        pass

    @abstractmethod
    async def turn_off(self):
        """Turn the device off."""
        pass

    @property
    def mac(self):
        return self._mac
