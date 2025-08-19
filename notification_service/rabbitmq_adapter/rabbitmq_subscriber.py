import asyncio
import json

from notification_service.rabbitmq_adapter.rabbitmq_adapter import \
    RabbitMqAdapter


class RabbitMqSubscriber(RabbitMqAdapter):
    async def amqp_handler(self, callback):
        await self.connect()
        async with self._channel_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    asyncio.create_task(callback(payload))
