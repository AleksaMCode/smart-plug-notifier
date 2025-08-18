import json

import aio_pika

from rabbitmq_adapter.rabbitmq_adapter import RabbitMqAdapter


class RabbitMqPublisher(RabbitMqAdapter):
    async def amqp_handler(self, message: dict):
        await self.connect()
        body = json.dumps(message).encode()
        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=body,
                # in-memory only
                delivery_mode=aio_pika.DeliveryMode.NOT_PERSISTENT,
            ),
            routing_key=self._queue,
        )
