import os

from dotenv import load_dotenv

# Load .env file (if exists)
load_dotenv()

# Environment variables for Rabbit MQ
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

# Environment variable for Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

if not RABBITMQ_USERNAME or not RABBITMQ_USERNAME:
    raise RuntimeError(
        "RABBITMQ_USERNAME and RABBITMQ_PASSWORD must be set in .env or environment variables."
    )

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID must be set in .env or environment variables."
    )

# Pause between resuming operation (retry to connect or search for something)
SLEEP_TIME = 10

# Server configuration.
SERVER = {
    # localhost address is needed to make `uvicorn` server accessible on the local network using different devices.
    "localhost": "0.0.0.0",
    "host": "127.0.0.1",
    "port": 3_002,
}

# Rabbit MQ configuration.
RABBIT_MQ = {
    "host": "localhost",
    "port": 5672,
    "queue": "smart_device",
}
