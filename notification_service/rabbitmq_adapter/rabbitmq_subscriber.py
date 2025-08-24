import asyncio
import json

from rabbitmq_adapter.rabbitmq_adapter import RabbitMqAdapter
from yaspin import yaspin


class RabbitMqSubscriber(RabbitMqAdapter):
    @yaspin(text=f"Reading messages from RabbitMQ...")
    async def amqp_handler(self, callback):
        await self.connect()
        async with self._channel_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    asyncio.create_task(callback(payload))
