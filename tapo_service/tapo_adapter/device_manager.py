import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

from settings import DEVICE_LIST
from tapo import ApiClient
from tapo_adapter.device_factory import DeviceFactory
from tapo_adapter.plug_p110 import PlugP110
from tapo_adapter.tapo_device_type import TapoDeviceType


@dataclass
class ManagedDevice:
    device: PlugP110
    task: Optional[asyncio.Task] = None


class DeviceManager:
    """Manages multiple Tapo devices asynchronously."""

    def __init__(self):
        self.devices: Dict[str, ManagedDevice] = {}

    async def add_device(self, name: str, device: PlugP110):
        self.devices[name] = ManagedDevice(device=device)
        print(f"Added device '{name}' with MAC {device.mac}")

    def get_device(self, name: str) -> PlugP110:
        return self.devices.get(name).device if name in self.devices else None

    async def turn_on_all(self):
        await asyncio.gather(
            *(managed.device.turn_on() for managed in self.devices.values())
        )

    async def turn_off_all(self):
        await asyncio.gather(
            *(managed.device.turn_off() for managed in self.devices.values())
        )

    async def start_pooling(self):
        await self.turn_on_all()
        """Start notifier tasks for all devices concurrently."""
        for name, managed in self.devices.items():
            if managed.task is None:
                managed.task = asyncio.create_task(managed.device.pooling())

    async def stop_pooling(self):
        """Cancel all notifier tasks."""
        for managed in self.devices.values():
            if managed.task:
                managed.task.cancel()
                managed.task = None

    def save_states(self):
        """Persist the last known state of all devices."""
        for dev in self.devices.values():
            try:
                dev.device.save_state()
            except Exception as e:
                print(f"[{dev.device.mac}] Failed to save state: {e}")
        print("Saved all device states.")


class DeviceManagerBuilder:
    """Builds a DeviceManager from configuration."""

    def __init__(self, client: ApiClient):
        self._client = client

    async def build(self) -> DeviceManager:
        manager = DeviceManager()
        for name, mac in DEVICE_LIST.items():
            # For now, only PlugP110 is supported
            device = await DeviceFactory.create(
                name, TapoDeviceType.P110, mac, self._client
            )
            await manager.add_device(name, device)
        return manager
