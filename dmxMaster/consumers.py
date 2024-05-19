# chat/consumers.py
import json
import string

import channels.layers
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from dmxMaster.comunicationHelper import set_mixer_online, addPagesIfNotExisting, newPage
from django.conf import settings

from prismdmx.settings import MIXER_GROUP_NAME
from .databaseHelper import get_loaded_project, get_mixer_page
from .models import Fixture, Template, Mixer, Project, MixerPage

from dmxMaster.comunicationHelper import getAllFixturesAndTemplates, addFixture, editFixture, deleteFixture, setProject, \
    deleteProject, newProject, editFader, deletePage, setMixerColor


#OVERVIEW_GROUP_NAME = "OVERVIEWGroup"
#CONNECTED_GROUP_NAME = "CONNECTEDGroup"
def broadcast(content, group):
    if type(content) is not str:
        print("notString")
        content = json.dumps(content)
    print(content)
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

        self.channel_layer.group_add(settings.OVERVIEW_GROUP_NAME, self.channel_name)

        self.accept()
        self.send(json.dumps(getAllFixturesAndTemplates(True)))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(#langsam
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
                deletePage(text_data_json)
            if "deletePage" in text_data:
                deletePage(text_datas_json)
            if "editMixerFader" in text_data:
                editFader(text_data_json)
                updateDisplayText()
            if "setMixerColor" in text_data:
                setMixerColor(text_data_json)
                updateMixerColor()


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
        #4 Prefix, 2 Display, ... contend
        self.send("disp01 ")
        set_mixer_online(True)
        push_all_data()
        updateDisplayText()
        updateMixerColor()


    def disconnect(self, close_code):
        # Leave room group asdasdasd
        async_to_sync(self.channel_layer.group_discard)(
            settings.MIXER_GROUP_NAME,
            self.channel_name
        )
        set_mixer_online(False)
        push_all_data()

    def new_content(self, event):
        self.send(event['content'])
    def receive(self, text_data):
        print(text_data)

        try:
            text_data_json = json.loads(text_data)




        except ValueError as e:
           # self.send("NO VALID JSON")
            return



#MixerHelper

def updateDisplayText():
    mixer_page = MixerPage.objects.get(id=get_mixer_page())
    faders = mixer_page.mixerfader_set.all()
    index = 0
    for fader in faders:
        broadcast(str("disp"+ str(index) + fader.name), MIXER_GROUP_NAME)
        index += 1
def updateMixerColor():
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0].color

    color = tuple(int(mixer[i:i+2], 16) for i in (0, 2, 4))
    broadcast(str("colr" + str(color[0])), MIXER_GROUP_NAME)
    broadcast(str("colg" + str(color[1])), MIXER_GROUP_NAME)
    broadcast(str("colb" + str(color[2])), MIXER_GROUP_NAME)