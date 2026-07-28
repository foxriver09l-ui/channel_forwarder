import asyncio
from flask import Flask, send_file
from threading import Thread

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import TOKEN
from database import create_tables
from handlers import (
    start,
    help_command,
    add_channel,
    remove_channel,
    list_channels,
    receive_post
)

app_web = Flask(__name__)


@app_web.route("/download-db")
def download_db():

    return send_file(
        "bot.db",
        as_attachment=True
    )


def run_web():

    app_web.run(
        host="0.0.0.0",
        port=10000
    )
async def main():

    create_tables()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
    CommandHandler(
        "help",
        help_command
    )
    )

    app.add_handler(
        CommandHandler(
            "addchannel",
            add_channel
        )
    )

    app.add_handler(
        CommandHandler(
            "removechannel",
            remove_channel
        )
    )

    app.add_handler(
        CommandHandler(
            "channels",
            list_channels
        )
    )

    app.add_handler(
        MessageHandler(
            (
                filters.TEXT
                | filters.PHOTO
                | filters.VIDEO
                | filters.Document.ALL
            )
            & ~filters.COMMAND,
            receive_post
        )
    )

    print("Bot running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())