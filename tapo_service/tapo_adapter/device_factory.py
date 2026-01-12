from abc import ABCMeta

from rabbitmq_adapter.rabbitmq_adapter import RabbitMqAdapter
from tapo import ApiClient
from tapo_adapter.device import Device
from tapo_adapter.plug_p110 import PlugP110
from tapo_adapter.tapo_device_type import TapoDeviceType


class DeviceFactory(metaclass=ABCMeta):
    """Abstract factory for Tapo devices."""

    @staticmethod
    async def create(
        name: str,
        type: TapoDeviceType,
        client: ApiClient,
        rabbitmq: RabbitMqAdapter,
        *,
        mac: str,
        ip: str = None
    ) -> Device:
        match type:
            case TapoDeviceType.P110:
                device = PlugP110(name, client, rabbitmq, mac, ip)
                await device.init()
                return device
            case _:
                raise RuntimeError(f"Unsupported device type: {type}")
