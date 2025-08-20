import asyncio
import json

from settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, SLEEP_TIME
from telegram import Bot


class TelegramAdapter:
    def __init__(
        self, token: str = None, chat_id: str = None, messages_file: str = "en.json"
    ):
        self._chat_id = chat_id or TELEGRAM_CHANNEL_ID
        self._bot = Bot(token=token or TELEGRAM_BOT_TOKEN)
        self._messages = {}
        if messages_file:
            with open(messages_file, "r") as file:
                self._messages = json.load(file)

    async def send_message(self, name: str, state: bool):
        """
        Send a message based on a device state.
        True -> started, False -> finished
        """
        key = "started" if state else "finished"
        template = self._messages.get(key)
        if not template:
            return
        text = template.format(name)
        for i in range(10):
            try:
                await self._bot.send_message(chat_id=self._chat_id, text=text)
                break
            except Exception:
                await asyncio.sleep(SLEEP_TIME)
        else:
            raise RuntimeError("Failed to send a message to the Telegram channel.")
