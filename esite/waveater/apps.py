# -*- coding: utf-8 -*-
import os
import io
import logging
import json
import hashlib
import uuid

from django.conf import settings
from django.apps import AppConfig
from django.core.files import File
from django.contrib.auth import get_user_model

from telethon import TelegramClient, events, functions
from .file_handler import progress
import os
import time
import datetime
import asyncio
import threading
from asgiref.sync import sync_to_async


api_key = "avycptv52dv8lhn9mj8mn"

# Allows adding as many coins as desired
coin_list = [
    "DOGE",
    "ETH",
    "BTC"
]

coins = ','.join(coin_list)

config = [
    {"symbol": ""},
    {"name": " Name: "},
    {"price_btc": " Price in BTC: "},
    {"price": " Price: "},
    {"percent_change_24h": " - 24 Hour Percent Change: "},
    {"market_cap": " Market Cap: "},
    {"volume_24h": " 24 Hour Volume: "},
    {"url_shares": " URL Shares: "},
    {"reddit_posts": " Reddit Posts: "},
    {"tweets": " Tweets: "},
    {"news": " News: "},
]

# config = [
#     {"symbol": ""},
#     {"price_btc": " Price in BTC: "},
#     {"price": " Price: "},
#     {"percent_change_24h": " - 24 Hour Percent Change: "},
#     {"market_cap": " Market Cap: "},
#     {"volume_24h": " 24 Hour Volume: "},
#     {"url_shares": " URL Shares: "},
#     {"reddit_posts": " Reddit Posts: "},
#     {"tweets": " Tweets: "},
#     {"galaxy_score": " Galaxy Score: "},
#     {"volatility": " Volatility: "},
#     {"social_volume": " Social Volume: "},
#     {"news": " News: "},
# ]


@sync_to_async
def to_info_string(asset_coin, value, key, asset):
    
    if key == 'symbol':
        asset_coin += " (" + asset[key] + ")" + "\n"
    elif key == 'percent_change_24h':
        asset_coin += f"**{value}**" + str(asset[key]) + "%" + "\n"
    else:
        asset_coin += f"**{value}**" + str(asset[key]) + "\n"
    return asset_coin

class WaveaterConfig(AppConfig):
    name = "esite.waveater"

    def ready(self):
        """Start the client."""
        print("waveaterbot started...")
        waveater_thread = threading.Thread(
            name="waveater-main-thread", target=Waveater.main
        )
        waveater_thread.daemon = False  # -> dies after main thread is closed
        waveater_thread.start()


class Waveater:
    def main():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(
            "client", settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH, loop=loop
        ).start(bot_token=settings.TELEGRAM_BOT_TOKEN)

        @client.on(events.NewMessage(pattern="/start"))
        @client.on(events.NewMessage(pattern="/help"))
        async def start(event):
            """Send a message when the command /start is issued."""
            await event.respond(
                "Hi, I'm an audio slave! :3\nI would love to convert every wav you got into a telegram voice message. (>.<)"
            )
            raise events.StopPropagation

        @client.on(events.NewMessage(pattern="/motivation"))
        async def start(event):
            """Send a message when the command /start is issued."""
            await event.respond(
                "OMG! Senpai, *o* let me convewt some wav into telegwam voice message, ~Nyaaaa"
            )
            raise events.StopPropagation

        @client.on(events.NewMessage(pattern="/all"))
        async def handle(event):
            import urllib.request
            import ssl
            import json

            url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + coins
            assets = json.loads(urllib.request.urlopen(url).read())

            asset_indicator = ""

            for asset in assets['data']:
                asset_coin = ""
                
                for field in config:
                    key = list(field.keys())[0]
                    value = list(field.values())[0]
                    asset_coin = await to_info_string(asset_coin, value, key, asset)

                    if key == 'percent_change_24h':
                        if value != "-":
                            asset_indicator = "✅ "
                        else:
                            asset_indicator = "🔻 "

                await event.respond(
                    asset_indicator + asset_coin
                )

        @client.on(events.NewMessage(pattern="/btc"))
        async def handle(event):
            import urllib.request
            import ssl
            import json

            url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + "BTC"
            assets = json.loads(urllib.request.urlopen(url).read())

            asset_indicator = ""

            for asset in assets['data']:
                asset_coin = ""
                
                for field in config:
                    key = list(field.keys())[0]
                    value = list(field.values())[0]
                    asset_coin = await to_info_string(asset_coin, value, key, asset)

                    if key == 'percent_change_24h':
                        if value != "-":
                            asset_indicator = "✅ "
                        else:
                            asset_indicator = "🔻 "

                await event.respond(
                    asset_indicator + asset_coin
                )

        @client.on(events.NewMessage(pattern="/doge"))
        async def handle(event):
            import urllib.request
            import ssl
            import json

            url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + "DOGE"
            assets = json.loads(urllib.request.urlopen(url).read())

            asset_indicator = ""

            for asset in assets['data']:
                asset_coin = ""
                
                for field in config:
                    key = list(field.keys())[0]
                    value = list(field.values())[0]
                    asset_coin = await to_info_string(asset_coin, value, key, asset)

                    if key == 'percent_change_24h':
                        if value != "-":
                            asset_indicator = "✅ "
                        else:
                            asset_indicator = "🔻 "

                await event.respond(
                    asset_indicator + asset_coin
                )

        @client.on(events.NewMessage(pattern="/eth"))
        async def handle(event):
            import urllib.request
            import ssl
            import json

            url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + "ETH"
            assets = json.loads(urllib.request.urlopen(url).read())

            asset_indicator = ""

            for asset in assets['data']:
                asset_coin = ""
                
                for field in config:
                    key = list(field.keys())[0]
                    value = list(field.values())[0]
                    asset_coin = await to_info_string(asset_coin, value, key, asset)

                    if key == 'percent_change_24h':
                        if value != "-":
                            asset_indicator = "✅ "
                        else:
                            asset_indicator = "🔻 "

                await event.respond(
                    asset_indicator + asset_coin
                )

        @client.on(events.NewMessage(pattern="/snek"))
        async def handle(event):
            import urllib.request
            import ssl
            import json

            url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + "ETH"
            assets = json.loads(urllib.request.urlopen(url).read())

            asset_indicator = ""

            for asset in assets['data']:
                asset_coin = ""
                
                for field in config:
                    key = list(field.keys())[0]
                    value = list(field.values())[0]
                    asset_coin = await to_info_string(asset_coin, value, key, asset)

                    if key == 'percent_change_24h':
                        if value != "-":
                            asset_indicator = "✅ "
                        else:
                            asset_indicator = "🔻 "

                await event.respond(
                    f"""✅  (SNEK)
                **Name:** SnekCoin
                **Price in BTC:** 0.000000000000e-39
                **Price:** 0.000000
                - **24 Hour Percent Change:** 100%
                **Market Cap:** 0
                **24 Hour Volume:** 0.00
                **URL Shares:** 1
                **Reddit Posts:** 0
                **Tweets:** 1
                **News:** 0"""
                )


        with client:
            client.run_until_disconnected()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 miraculix-org Florian Kleber
