# chat/consumers.py
import json

import channels.layers
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.conf import settings
from .models import Fixture, Template, Mixer

from dmxMaster.comunicationHelper import getAllFixturesAndTemplates, addFixture, editFixture, deleteFixture, setProject, \
    deleteProject, newProject


def broadcast_content(content):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.MAIN_GROUP_NAME, {
            "type": 'new_content',
            "content": json.dumps(content),
        })


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            settings.MAIN_GROUP_NAME,
            self.channel_name
        )

        self.accept()

        self.send(json.dumps(getAllFixturesAndTemplates(True)))

    def disconnect(self, close_code):
        # Leave room group asdasdasd
        async_to_sync(self.channel_layer.group_discard)(
            settings.MAIN_GROUP_NAME,
            self.channel_name
        )

    def new_content(self, event):
        self.send(event['content'])

    def receive(self, text_data):
        print(text_data)
        if "test" == text_data:
            broadcast_content("getAllFixturesAndTemplates()")
            return

        if "test2" == text_data:
            allMixers = Mixer.objects.all()

            for x in allMixers:
                self.send(json.dumps(x.generateJson()))

            return

        try:
            text_data_json = json.loads(text_data)
            if "newFixture" in text_data:
                addFixture(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(False))
            if "editFixture" in text_data:
                editFixture(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(False))
            if "deleteFixture" in text_data:
                deleteFixture(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(False))
            if "setProject" in text_data:
                setProject(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(False))
            if "deleteProject" in text_data:
                deleteProject(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(False))
            if "newProject" in text_data:
                newProject(text_data_json)
                broadcast_content(getAllFixturesAndTemplates(True))

        except ValueError as e:
            self.send("NO VALID JSON")
            return
