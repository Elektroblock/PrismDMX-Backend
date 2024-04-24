# chat/consumers.py
import json

import channels.layers
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.conf import settings


def broadcast_content(content):
    channel_layer = channels.layers.get_channel_layer()
    channel_layer.group_send(
        settings.MAIN_GROUP_NAME, {
            "type": 'new_content',
            "content": json.dumps(content),
        })


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.channel_layer.group_add(
            settings.MAIN_GROUP_NAME,
            self.channel_name
        )

        self.accept()
        self.send("")

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            settings.MAIN_GROUP_NAME,
            self.channel_name
        )

    def new_content(self, event):
        self.send(event['content'])

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except ValueError as e:
            self.send("NO VALID JSON")
            return


        broadcast_content(text_data_json)
