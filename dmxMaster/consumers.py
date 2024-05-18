# chat/consumers.py
import json
import string

import channels.layers
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from dmxMaster.comunicationHelper import set_mixer_online, addPagesIfNotExisting, newPage
from django.conf import settings

from prismdmx.settings import MIXER_GROUP_NAME
from .models import Fixture, Template, Mixer

from dmxMaster.comunicationHelper import getAllFixturesAndTemplates, addFixture, editFixture, deleteFixture, setProject, \
    deleteProject, newProject


#OVERVIEW_GROUP_NAME = "OVERVIEWGroup"
#CONNECTED_GROUP_NAME = "CONNECTEDGroup"
def broadcast(content, group):
    if type(content) is not string:
        print("notString")
        content = json.dumps(content)
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            "type": 'new_content',
            "content": content,
        })


def push_all_data():
    broadcast(getAllFixturesAndTemplates(False), settings.CONNECTED_GROUP_NAME)
    broadcast(getAllFixturesAndTemplates(True), settings.OVERVIEW_GROUP_NAME)


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        async_to_sync(self.channel_layer.group_add)(
            settings.OVERVIEW_GROUP_NAME,
            self.channel_name
        )

        self.accept()

        self.send(json.dumps(getAllFixturesAndTemplates(True)))

    def disconnect(self, close_code):
        # Leave room group asdasdasd
        async_to_sync(self.channel_layer.group_discard)(
            settings.OVERVIEW_GROUP_NAME,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            settings.CONNECTED_GROUP_NAME,
            self.channel_name
        )

    def new_content(self, event):
        self.send(event['content'])

    def receive(self, text_data):

        print(text_data)
        if  text_data.startswith('!'):
            broadcast(text_data.replace('!', '', 1), MIXER_GROUP_NAME)
            #broadcast_content("getAllFixturesAndTemplates()")
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
            if "editFixture" in text_data:
                editFixture(text_data_json)
            if "deleteFixture" in text_data:
                deleteFixture(text_data_json)
            if "setProject" in text_data:

                if setProject(text_data_json):
                    async_to_sync(self.channel_layer.group_add)(
                        settings.CONNECTED_GROUP_NAME,
                        self.channel_name
                    )
                    async_to_sync(self.channel_layer.group_discard)(
                        settings.OVERVIEW_GROUP_NAME,
                        self.channel_name
                    )
                    addPagesIfNotExisting()
                else:
                    self.send(
                        '{"fixtureTemplates": [], "fixtures": [], "fixtureGroups": [],"mixer": {"color": "#000000", "mixerType": "na", "isMixerAvailable": "false", "pages": []},"project": {"name": "naa", "internalID": "naa"}}')

            if "deleteProject" in text_data:
                async_to_sync(self.channel_layer.group_add)(
                    settings.OVERVIEW_GROUP_NAME,
                    self.channel_name
                )
                async_to_sync(self.channel_layer.group_discard)(
                    settings.CONNECTED_GROUP_NAME,
                    self.channel_name
                )
                deleteProject(text_data_json)
            if "newProject" in text_data:
                newProject(text_data_json)
            if "newPage" in text_data:
                newPage()
            if "deletePage" in text_data:
                deletePage(json)

            push_all_data()


        except ValueError as e:
            self.send("NO VALID JSON")
            return


class MixerConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            settings.MIXER_GROUP_NAME,
            self.channel_name
        )

        self.accept()

        self.send("HI!")
        set_mixer_online(True)


    def disconnect(self, close_code):
        # Leave room group asdasdasd
        async_to_sync(self.channel_layer.group_discard)(
            settings.MIXER_GROUP_NAME,
            self.channel_name
        )
        set_mixer_online(False)

    def new_content(self, event):
        self.send(event['content'])
    def receive(self, text_data):
        print(text_data)

        try:
            text_data_json = json.loads(text_data)




        except ValueError as e:
           # self.send("NO VALID JSON")
            return
