import os

from dotenv import load_dotenv

# Load .env file (if exists)
load_dotenv()

# Environment variables for Tapo API
TAPO_EMAIL = os.getenv("TAPO_EMAIL")
TAPO_PASSWORD = os.getenv("TAPO_PASSWORD")

# Environment variables for Rabbit MQ
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

if not TAPO_EMAIL or not TAPO_PASSWORD:
    raise RuntimeError(
        "TAPO_EMAIL and TAPO_PASSWORD must be set in .env or environment variables."
    )

if not RABBITMQ_USERNAME or not RABBITMQ_USERNAME:
    raise RuntimeError(
        "RABBITMQ_USERNAME and RABBITMQ_PASSWORD must be set in .env or environment variables."
    )

# Network mask used to discover devices - used as a Target protocol address (TPA) for ARP messages
# E.g., 192.168.1.1/24
NETWORK_MASK = ""

# List of devices and their names
DEVICE_LIST = {"device1": "mac_address1", "device2": "mac_address2"}

# Pause between checking the power usage of a device
DEVICE_SLEEP_TIME = 5

# Max attempts if not successful
MAX_ATTEMPT = 5

# Pause between resuming operation (retry to connect or search for something)
SLEEP_TIME = 10

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
