import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from notification_service.telegram_adapter import TelegramAdapter
from rabbitmq_subscriber import RabbitMqSubscriber
from starlette.middleware.cors import CORSMiddleware

from notification_service.settings import (RABBIT_MQ, RABBITMQ_PASSWORD,
                                           RABBITMQ_USERNAME, SERVER)

origins = ["*"]
rabbitmq: RabbitMqSubscriber = None
telegram: TelegramAdapter = None


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    print("Server starting.")
    yield
    print("Server shutting down.")


async def handle_payload(payload: dict):
    print(f"Received message: {payload}")
    await telegram.send_message(payload.get("device"), payload.get("state"))


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init():
    global rabbitmq, telegram
    rabbitmq = RabbitMqSubscriber(
        host=RABBIT_MQ["host"],
        port=RABBIT_MQ["port"],
        queue=RABBIT_MQ["queue"],
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
    )
    telegram = TelegramAdapter()


async def serve_fastapi():
    config = uvicorn.Config(
        app, host=SERVER["localhost"], port=SERVER["port"], reload=False
    )
    server = uvicorn.Server(config)
    await server.serve()


async def serve_rabbitmq():
    await rabbitmq.amqp_handler(handle_payload)


async def main():
    await init()
    print("RabbitMQ subscriber running.")
    await asyncio.gather(serve_fastapi(), serve_rabbitmq())


if __name__ == "__main__":
    asyncio.run(main())
