from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden

from database import (
    register_user,
    add_channel as db_add_channel,
    remove_channel as db_remove_channel,
    get_channels,
    channel_exists,
)

from utils import modify_post

# ---------------- START ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    register_user(update.effective_user)

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "1. Add your channels:\n"
        "/addchannel @mychannel\n\n"
        "2. Add me as admin in those channels.\n\n"
        "3. Send me any post and I'll publish it."
    )


# ---------------- ADD CHANNEL ---------------- #

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    register_user(update.effective_user)

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/addchannel @channel"
        )
        return


    username = context.args[0]


    if not username.startswith("@"):
        username = "@" + username


    # Check channel exists

    try:

        chat = await context.bot.get_chat(username)

    except BadRequest:

        await update.message.reply_text(
            "❌ Channel not found."
        )
        return


    except Exception:

        await update.message.reply_text(
            "❌ Cannot access this channel."
        )
        return



    # Check duplicate

    if channel_exists(
        update.effective_user.id,
        chat.id
    ):

        await update.message.reply_text(
            "❌ This channel is already added."
        )

        return



    # Check bot admin

    bot = await context.bot.get_me()


    try:

        member = await context.bot.get_chat_member(
            chat.id,
            bot.id
        )


    except (Forbidden, BadRequest):

        await update.message.reply_text(
            "❌ Add me as administrator in the channel first."
        )

        return



    if member.status != "administrator":

        await update.message.reply_text(
            "❌ I must be administrator in the channel."
        )

        return



    # Save

    db_add_channel(
        telegram_id=update.effective_user.id,
        channel_id=chat.id,
        username=username,
        tag=username
    )


    await update.message.reply_text(
        f"✅ Added {username}"
    )

# ---------------- REMOVE CHANNEL ---------------- #

async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage:\n"
            "/removechannel @channel"
        )
        return

    channel = context.args[0]

    if not channel.startswith("@"):
        channel = "@" + channel

    db_remove_channel(
        update.effective_user.id,
        channel
    )

    await update.message.reply_text(
        f"🗑 Removed {channel}"
    )


# ---------------- LIST CHANNELS ---------------- #

async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    channels = get_channels(update.effective_user.id)

    if not channels:

        await update.message.reply_text(
            "You don't have any channels."
        )

        return

    text = "📢 Your channels:\n\n"

    for i, (_, username, tag) in enumerate(channels, start=1):

        text += f"{i}. {username}\n"

    await update.message.reply_text(text)


# ---------------- RECEIVE POST ---------------- #

async def receive_post(update: Update, context: ContextTypes.DEFAULT_TYPE):

    register_user(update.effective_user)

    channels = get_channels(update.effective_user.id)

    if not channels:

        await update.message.reply_text(
            "❌ You don't have any channels.\n\n"
            "Use:\n"
            "/addchannel @yourchannel"
        )

        return

    # Get message text

    if update.message.text:

        original_text = update.message.text

    elif update.message.caption:

        original_text = update.message.caption

    else:

        original_text = ""

    clean_text = modify_post(original_text)

    success = 0
    failed = 0

    # ---------------- PHOTO ---------------- #

    if update.message.photo:

        for channel_id, username, tag in channels:

            caption = clean_text

            if caption:
                caption += f"\n\n📢 {tag}"
            else:
                caption = f"📢 {tag}"

            try:

                await context.bot.send_photo(
                    chat_id=channel_id,
                    photo=update.message.photo[-1].file_id,
                    caption=caption
                )

                success += 1

            except Exception as e:

                print(e)
                failed += 1

    # ---------------- VIDEO ---------------- #

    elif update.message.video:

        for channel_id, username, tag in channels:

            caption = clean_text

            if caption:
                caption += f"\n\n📢 {tag}"
            else:
                caption = f"📢 {tag}"

            try:

                await context.bot.send_video(
                    chat_id=channel_id,
                    video=update.message.video.file_id,
                    caption=caption
                )

                success += 1

            except Exception as e:

                print(e)
                failed += 1

    # ---------------- DOCUMENT ---------------- #

    elif update.message.document:

        for channel_id, username, tag in channels:

            caption = clean_text

            if caption:
                caption += f"\n\n📢 {tag}"
            else:
                caption = f"📢 {tag}"

            try:

                await context.bot.send_document(
                    chat_id=channel_id,
                    document=update.message.document.file_id,
                    caption=caption
                )

                success += 1

            except Exception as e:

                print(e)
                failed += 1

    # ---------------- TEXT ---------------- #

    else:

        for channel_id, username, tag in channels:

            message = clean_text

            if message:
                message += f"\n\n📢 {tag}"
            else:
                message = f"📢 {tag}"

            try:

                await context.bot.send_message(
                    chat_id=channel_id,
                    text=message
                )

                success += 1

            except Exception as e:

                print(e)
                failed += 1

    await update.message.reply_text(
        f"✅ Sent: {success}\n"
        f"❌ Failed: {failed}"
    )