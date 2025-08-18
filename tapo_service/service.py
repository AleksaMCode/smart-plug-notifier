import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import (RABBIT_MQ, RABBITMQ_PASSWORD, RABBITMQ_USERNAME, SERVER,
                      TAPO_EMAIL, TAPO_PASSWORD)
from tapo import ApiClient
from tapo_adapter.device_manager import DeviceManager, DeviceManagerBuilder

from tapo_service.rabbitmq_publisher import RabbitMqPublisher

origins = ["*"]
api_client = None
device_manager: DeviceManager = None
rabbitmq: RabbitMqPublisher = None


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    print("Server starting.")
    global api_client, device_manager
    yield
    print("Server shutting down.")
    if device_manager:
        await device_manager.stop_pooling()
    device_manager.save_states()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init():
    global api_client, device_manager, rabbitmq
    api_client = ApiClient(TAPO_EMAIL, TAPO_PASSWORD)
    rabbitmq = RabbitMqPublisher(
        host=RABBIT_MQ["host"],
        port=RABBIT_MQ["port"],
        queue=RABBIT_MQ["queue"],
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
    )
    await rabbitmq.connect()
    builder = DeviceManagerBuilder(api_client, rabbitmq)
    device_manager = await builder.build()


async def serve_fastapi():
    config = uvicorn.Config(
        app, host=SERVER["localhost"], port=SERVER["port"], reload=False
    )
    server = uvicorn.Server(config)
    await server.serve()


async def serve_device_manager():
    await device_manager.start_pooling()


async def main():
    await init()
    print("Device Manager initialized and notifiers running.")
    await asyncio.gather(serve_fastapi(), serve_device_manager())


if __name__ == "__main__":
    asyncio.run(main())
