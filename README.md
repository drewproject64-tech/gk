# SYARIKAT MY welcome bot

On `/start`, sends the supplied Malay welcome caption and four URL buttons in two rows: MY.CASH88 / GK9, then LUCKYEGG88 / MAHKOTA8.

## Upload your banner

Open https://github.com/drewproject64-tech/gk/upload/main/assets and upload the original banner as **welcome.jpg**, **welcome.jpeg**, or **welcome.png** (lowercase). Commit the upload to main. Upload only the banner, not a screenshot of the entire Telegram chat. Keep it under Telegram's 10 MB photo limit.

The bot reads the image from `assets/` and sends it as a photo with the welcome text as its caption. Until a banner exists, it sends the same text and buttons without a photo. Redeploy/restart from the latest commit after uploading the banner. Telegram controls button colours and chat backgrounds.

## Run

Requires Python 3.11 or newer. No third-party packages required.

1. Create a bot with @BotFather.
2. Set **BOT_TOKEN** as a secret environment variable on your host. Never commit the token.
3. Start command: `python bot.py`

For Render, use a **Background Worker**, build command `pip install -r requirements.txt`, start command `python bot.py`. Run one instance only because this bot uses long polling. This repository does not deploy itself.

## Checks

`python -m py_compile bot.py`

Live Telegram delivery requires a valid token and a running deployment.
