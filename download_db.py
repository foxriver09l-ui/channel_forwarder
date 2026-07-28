from flask import Flask, send_file

app = Flask(__name__)


@app.route("/download-db")
def download_db():

    return send_file(
        "bot.db",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )