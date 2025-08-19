import os

from dotenv import load_dotenv

# Load .env file (if exists)
load_dotenv()

# Environment variables for Rabbit MQ
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

if not RABBITMQ_USERNAME or not RABBITMQ_USERNAME:
    raise RuntimeError(
        "RABBITMQ_USERNAME and RABBITMQ_PASSWORD must be set in .env or environment variables."
    )

# Server configuration.
SERVER = {
    # localhost address is needed to make `uvicorn` server accessible on the local network using different devices.
    "localhost": "0.0.0.0",
    "host": "127.0.0.1",
    "port": 3_001,
}

# Rabbit MQ configuration.
RABBIT_MQ = {
    "host": "localhost",
    "port": 5672,
    "queue": "smart_device",
}
