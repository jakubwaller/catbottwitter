import os
import traceback
from random import random

from mastodon import Mastodon

import requests
import tweepy
from telegram import Bot
import asyncio

from tools import read_config, run_request

config = read_config()
cat_api_key = config["cat_api_key"]
telegram_chat_id = config["telegram_chat_id"]
telegram_bot_id = config["telegram_bot_id"]

try:
    auth = tweepy.OAuth1UserHandler(
        config['twitter_key'],
        config['twitter_secret'],
        config['twitter_token_key'],
        config['twitter_token_secret']
    )

    api = tweepy.API(auth)

    if random() < 0.5:
        image_type = "?mime_types=gif"
    else:
        image_type = "?mime_types=jpg,png"

    url = run_request(
        "GET",
        f"https://api.thecatapi.com/v1/images/search{image_type}",
        num_of_tries=5,
        request_headers={"Content-Type": "application/json", "x-api-key": cat_api_key},
    )[0]["url"]

    image_name = url.split("/")[-1]

    img_data = requests.get(url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)

    api.update_status_with_media("One #cat per day keeps the doctor away. #catsoftwitter", image_name)

    mastodon = Mastodon(access_token=config["mastodon_token"], api_base_url="hostux.social")
    mastodon_media = mastodon.media_post(image_name)
    mastodon.status_post('One #cat per day keeps the doctor away. #catsofmastodon', media_ids=mastodon_media["id"])

    os.remove(image_name)

    bot = Bot(telegram_bot_id)

    if url.endswith(".gif"):
        asyncio.run(bot.send_animation(telegram_chat_id, url))
    else:
        asyncio.run(bot.send_photo(telegram_chat_id, url))
except Exception as exc:
    print(exc)
    traceback.print_exc()
