import json
from io import BytesIO

import requests
import requests as r
from flask import Flask, request
from PIL import Image
from requests import post

from config import BOT_TKN
from model_inference import predict_species

BOT_KEY = f"bot{BOT_TKN}"
BASE_URL = f"https://api.telegram.org/"
SEND_URL = f"{BASE_URL}{BOT_KEY}/sendMessage"
ACTN_URL = f"{BASE_URL}{BOT_KEY}/sendChatAction"
FILE_URL = f"{BASE_URL}{BOT_KEY}/getFile?file_id="
DOWN_URL = f"{BASE_URL}/file/{BOT_KEY}/"

app = Flask(__name__)


def send_message(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text,
    }
    _ = post(SEND_URL, params=params)


def send_greeting(chat_id):
    send_message(
        chat_id,
        "Welcome to the Birdwatcher KG Chat Bot!\n\n Please send a photo of a bird you want to be recognised.",
    )


def send_typing(chat_id):
    params = {
        "chat_id": chat_id,
        "action": "typing",
    }
    _ = post(ACTN_URL, params=params)


def get_photo(photo_id):
    res = r.get(FILE_URL + photo_id)
    file_path = res.json()["result"]["file_path"]

    if (
        file_path.endswith("jpg")
        or file_path.endswith("jpeg")
        or file_path.endswith("png")
    ):
        url = DOWN_URL + file_path
        print(url)
        res = r.get(url)
        return BytesIO(res.content)


@app.route("/", methods=["GET", "POST"])
def hw():  # sourcery skip: last-if-guard
    if request.method != "POST":
        return "All good"

    message = request.get_json()["message"]
    chat = message["chat"]

    if "photo" not in message:
        send_greeting(chat["id"])
        return "received"

    send_typing(chat["id"])
    photo = message["photo"][-1]
    photo_obj = get_photo(photo["file_id"])
    prediction = predict_species(photo_obj)
    send_message(chat["id"], prediction)
    return "received"


@app.route("/message", methods=["POST"])
def message():
    return request.form


if __name__ == "__main__":
    app.run(debug=True)
