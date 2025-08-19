from abc import ABCMeta, abstractmethod

import aio_pika


class RabbitMqAdapter(metaclass=ABCMeta):
    """Abstract base class for RabbitMQ operations with default init and connect."""

    _connection: aio_pika.RobustConnection = None
    _channel: aio_pika.RobustChannel = None
    """
    Channel name
    """
    _channel_queue: aio_pika.abc.AbstractRobustQueue = None
    """
    Actual RabbitMQ channel
    """

    def __init__(self, host: str, port: int, queue: str, username: str, password: str):
        self._host = host
        self._port = port
        self._queue = queue
        self._username = username
        self._password = password

    async def connect(self) -> None:
        """Default connection logic to RabbitMQ."""
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._username,
                password=self._password,
            )
            self._channel = await self._connection.channel()
            # not durable → doesn't survive broker restart
            # auto_delete → deleted once no subscribers remain
            self._channel_queue = await self._channel.declare_queue(
                self._queue,
                durable=True,
                # durable=False, auto_delete=True
            )

    @abstractmethod
    async def amqp_handler(self, message: dict):
        """Subclasses should implement sending or receiving logic."""
        pass
