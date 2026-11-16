"""SYARIKAT MY Telegram welcome bot (Python standard library only)."""
import json
import logging
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

WELCOME = """WELCOME TO SYARIKAT MY

⚡️4 JENAMA • 1 KELUARGA
⚡️BERSATU BERSAMA 4DGANG
⚡️4 JENAMA • 1 DESTINASI
━━━━━━━━━━━━━━━━━━

⭐️ Kenali Jenama Kami & Terokai Lebih Banyak Pilihan!
⭐️ DI BAWAH NAUNGAN 4DGANG GROUP

⬇️ PILIH JENAMA KEGEMARAN ANDA DI BAWAH! ⬇️"""

KEYBOARD = {"inline_keyboard": [
    [{"text": "MY.CASH88", "url": "https://mycash88.com/RFTELEGRAMADS"},
     {"text": "GK9", "url": "https://gk9gk9.com/RFTELEGRAMADS"}],
    [{"text": "LUCKYEGG88", "url": "https://luckyegg88.com/RFTELEGRAMADS"},
     {"text": "MAHKOTA8", "url": "https://mkt8.vip/RFTELEGRAMADS1"}],
]}
ROOT = Path(__file__).resolve().parent


class TelegramError(Exception):
    pass


class Telegram:
    def __init__(self, token):
        self.base = f"https://api.telegram.org/bot{token}/"

    def call(self, method, data):
        request = Request(self.base + method, data=json.dumps(data).encode(),
                          headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=45) as response:
                result = json.load(response)
        except HTTPError as error:
            # Never log the request URL: it contains the bot token.
            raise TelegramError(f"Telegram HTTP {error.code}") from None
        except (URLError, TimeoutError, OSError):
            raise TelegramError("Telegram connection failed") from None
        if not result.get("ok"):
            raise TelegramError("Telegram request rejected")
        return result["result"]

    def send_welcome(self, chat_id):
        image = next((ROOT / "assets" / name for name in
                      ("welcome.jpg", "welcome.jpeg", "welcome.png")
                      if (ROOT / "assets" / name).is_file()), None)
        if image is None:
            self.call("sendMessage", {"chat_id": chat_id, "text": WELCOME,
                                     "reply_markup": KEYBOARD})
            return
        # Multipart upload sends the checked-out image, including in private repos.
        boundary = "SyarikatWelcomeBoundary"
        fields = {"chat_id": str(chat_id), "caption": WELCOME,
                  "reply_markup": json.dumps(KEYBOARD)}
        chunks = []
        for key, value in fields.items():
            chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; '
                           f'name="{key}"\r\n\r\n{value}\r\n').encode())
        mime = "image/png" if image.suffix == ".png" else "image/jpeg"
        chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; '
                       f'name="photo"; filename="{image.name}"\r\n'
                       f'Content-Type: {mime}\r\n\r\n').encode())
        chunks.extend([image.read_bytes(), f"\r\n--{boundary}--\r\n".encode()])
        request = Request(self.base + "sendPhoto", data=b"".join(chunks),
                          headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urlopen(request, timeout=45) as response:
                result = json.load(response)
        except HTTPError as error:
            raise TelegramError(f"Telegram image HTTP {error.code}") from None
        except (URLError, TimeoutError, OSError):
            raise TelegramError("Telegram image connection failed") from None
        if not result.get("ok"):
            raise TelegramError("Telegram image rejected")


def handle_update(bot, update):
    message = update.get("message", {})
    text = message.get("text", "")
    command = text.split(maxsplit=1)[0].split("@")[0] if text else ""
    if command == "/start":
        bot.send_welcome(message["chat"]["id"])


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("Set BOT_TOKEN in your hosting environment before starting.")
    bot = Telegram(token)
    bot.call("deleteWebhook", {"drop_pending_updates": False})
    offset = None
    logging.info("Welcome bot started")
    while True:
        try:
            updates = bot.call("getUpdates", {"offset": offset, "timeout": 30,
                                             "allowed_updates": ["message"]})
            for update in updates:
                try:
                    handle_update(bot, update)
                except TelegramError as error:
                    logging.warning("Welcome delivery failed: %s", error)
                offset = update["update_id"] + 1
        except TelegramError as error:
            logging.warning("Polling failed: %s", error)
            time.sleep(5)


if __name__ == "__main__":
    main()
