import asyncio
import json

import telegram
from settings import MAX_ATTEMPT, SLEEP_TIME, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from telegram import Bot
from tenacity import retry, stop_after_attempt, wait_fixed


class TelegramAdapter:
    def __init__(
        self, token: str = None, chat_id: str = None, messages_file: str = "en.json"
    ):
        self._chat_id = chat_id or TELEGRAM_CHANNEL_ID
        self._connect(token)
        self._messages = {}
        if messages_file:
            with open(messages_file, "r") as file:
                self._messages = json.load(file)

    @retry(
        wait=wait_fixed(SLEEP_TIME), stop=stop_after_attempt(MAX_ATTEMPT), reraise=True
    )
    def _connect(self, token: str = None):
        self._bot = Bot(token=token or TELEGRAM_BOT_TOKEN)

    @retry(
        wait=wait_fixed(SLEEP_TIME), stop=stop_after_attempt(MAX_ATTEMPT), reraise=True
    )
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
        try:
            await self._bot.send_message(chat_id=self._chat_id, text=text)
        except (telegram.error.TelegramError, ValueError):
            # TODO Log here
            print("Failed to send a message to the Telegram channel.")
            await asyncio.sleep(SLEEP_TIME)
