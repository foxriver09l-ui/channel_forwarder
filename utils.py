import re


def modify_post(text):

    if not text:
        text = ""

    text = re.sub(
        r"(https?://)?t\.me/\S+",
        "",
        text
    )

    text = re.sub(
        r"@[A-Za-z0-9_]+",
        "",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()