import sqlite3

db = sqlite3.connect(
    "bot.db",
    check_same_thread=False
)

cursor = db.cursor()


def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        telegram_id INTEGER PRIMARY KEY,

        username TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER NOT NULL,

        channel_id INTEGER NOT NULL,

        username TEXT NOT NULL,

        tag TEXT NOT NULL,

        UNIQUE(telegram_id, channel_id)
    )
    """)

    db.commit()


def register_user(user):

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username
        )
        VALUES
        (?,?)
        """,
        (
            user.id,
            user.username
        )
    )

    db.commit()


def add_channel(
    telegram_id,
    channel_id,
    username,
    tag
):

    cursor.execute(
        """
        INSERT INTO channels
        (
            telegram_id,
            channel_id,
            username,
            tag
        )
        VALUES
        (?,?,?,?)
        """,
        (
            telegram_id,
            channel_id,
            username,
            tag
        )
    )

    db.commit()


def remove_channel(
    telegram_id,
    username
):

    cursor.execute(
        """
        DELETE FROM channels
        WHERE telegram_id=?
        AND username=?
        """,
        (
            telegram_id,
            username
        )
    )

    db.commit()


def get_channels(
    telegram_id
):

    cursor.execute(
        """
        SELECT
            channel_id,
            username,
            tag
        FROM channels
        WHERE telegram_id=?
        ORDER BY username
        """,
        (
            telegram_id,
        )
    )

    return cursor.fetchall()


def channel_exists(
    telegram_id,
    channel_id
):

    cursor.execute(
        """
        SELECT 1
        FROM channels
        WHERE telegram_id=?
        AND channel_id=?
        LIMIT 1
        """,
        (
            telegram_id,
            channel_id
        )
    )

    return cursor.fetchone() is not None