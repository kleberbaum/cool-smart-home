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

from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from asgiref.sync import sync_to_async


client_id = 'paho-mqtt-python' + str(uuid.uuid4())
topic = "tele/mqtt-test/SENSOR"


def load_chunks(audio_in):
    audio_chunks = split_on_silence(audio_in, min_silence_len=1800, silence_thresh=-17)

    if audio_chunks:
        return audio_chunks
    else:
        return [
            audio_in,
        ]


@sync_to_async
def transcribe_audio(audio_in):
    for audio_chunk in load_chunks(audio_in):
        audio_chunk.export("temp", format="wav")

        with sr.AudioFile("temp") as source:
            audio = recognizer.listen(source)

            try:
                transcript = recognizer.recognize_google(
                    audio, language="de-AT", show_all=True
                )
                return transcript
            except Exception as ex:
                print("Error occured")
                print(ex)


@sync_to_async
def _audio_to_ow(
    chat_id,
    chat_title,
    track_audio_file,
    chat_description=None,
    tags=None,
    attendees=None,
    transcript=None,
):
    from django.contrib.auth.models import Group
    from esite.track.models import Track, ProjectAudioChannel
    

    pac, created = ProjectAudioChannel.objects.update_or_create(
        channel_id=chat_id,
        defaults={"title": chat_title, "description": chat_description},
    )

    track = Track.objects.create(
        pac=pac,
        title=track_audio_file.name,
        description=track_audio_file.description,
        audio_file=File(track_audio_file),
        audio_channel=track_audio_file.channel,
        audio_format=track_audio_file.format,
        audio_codec=track_audio_file.codec,
        audio_bitrate=track_audio_file.bitrate,
        tags=json.dumps([{"type": "tag", "value": tag} for tag in tags]),
        attendees=json.dumps(
            [{"type": "attendee", "value": attendee} for attendee in attendees]
        ),
        transcript=transcript,
    )

    if created:
        # pac has been created
        slavename = f"slave-{uuid.uuid4()}"
        password = get_user_model().objects.make_random_password()

        member = get_user_model().objects.create(username=slavename, is_active=True)
        member.set_password(hashlib.sha256(str.encode(password)).hexdigest())

        member.groups.add(Group.objects.get(name="ohrwurm-supervisor"))
        member.groups.add(Group.objects.get(name="ohrwurm-member"))

        member.pacs.add(pac)
        member.save()

        return f"Thx for joining Ohrwurm\nSlavename: {slavename}\nPassword: {password}"


class AsyncioHelper:
    def __init__(self, loop, client):
        self.loop = loop
        self.client = client
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.on_socket_register_write = self.on_socket_register_write
        self.client.on_socket_unregister_write = self.on_socket_unregister_write

    def on_socket_open(self, client, userdata, sock):
        print("Socket opened")

        def cb():
            print("Socket is readable, calling loop_read")
            client.loop_read()

        self.loop.add_reader(sock, cb)
        self.misc = self.loop.create_task(self.misc_loop())

    def on_socket_close(self, client, userdata, sock):
        print("Socket closed")
        self.loop.remove_reader(sock)
        self.misc.cancel()

    def on_socket_register_write(self, client, userdata, sock):
        print("Watching socket for writability.")

        def cb():
            print("Socket is writable, calling loop_write")
            client.loop_write()

        self.loop.add_writer(sock, cb)

    def on_socket_unregister_write(self, client, userdata, sock):
        print("Stop watching socket for writability.")
        self.loop.remove_writer(sock)

    async def misc_loop(self):
        print("misc_loop started")
        while self.client.loop_misc() == mqtt.MQTT_ERR_SUCCESS:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
        print("misc_loop finished")

class WaveaterConfig(AppConfig):
    name = "esite.waveater"

    def ready(self):
        """Start the client."""
        print("waveaterbot started...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Waveater(loop).main())
        loop.close()
        print("Finished")


class Waveater:
    def __init__(self, loop):
        self.loop = loop

    def on_connect(self, client, userdata, flags, rc):
        print("Subscribing")
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        if not self.got_message:
            print("Got unexpected message: {}".format(msg.decode()))
        else:
            self.got_message.set_result(msg.payload)

    def on_disconnect(self, client, userdata, rc):
        self.disconnected.set_result(rc)

    def main():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(
            "client", settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH, loop=loop
        ).start(bot_token=settings.TELEGRAM_BOT_TOKEN)

        self.disconnected = self.loop.create_future()
        self.got_message = None

        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)

        self.client.connect('10.1.0.1', 1883, 60)
        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

        for c in range(3):
            await asyncio.sleep(5)
            print("Publishing")
            self.got_message = self.loop.create_future()
            self.client.publish(topic, b'Hello' * 40000, qos=1)
            msg = await self.got_message
            print("Got response with {} bytes".format(len(msg)))
            self.got_message = None

        self.client.disconnect()
        print("Disconnected: {}".format(await self.disconnected))

        with client:
            client.run_until_disconnected()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 miraculix-org Florian Kleber
