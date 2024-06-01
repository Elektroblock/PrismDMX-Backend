# chat/consumers.py
import json
import math
import string

import channels.layers
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from dmxMaster.comunicationHelper import set_mixer_online, addPagesIfNotExisting, newPage, addFixtureToGroup, \
    removeFixtureFromGroup, editButton, newGroup, deleteGroup, selectFixture, deselectFixture, selectGroup, \
    deselectGroup
from django.conf import settings

from prismdmx.settings import MIXER_GROUP_NAME
from .databaseHelper import get_loaded_project, get_mixer_page, set_mixer_page, set_mixer_channel_page, \
    get_mixer_channel_page
from .models import Fixture, Template, Mixer, Project, MixerPage

from dmxMaster.comunicationHelper import addFixture, editFixture, deleteFixture, setProject, \
    deleteProject, newProject, editFader, deletePage, setMixerColor, get_template_json, get_meta_data
from datetime import datetime


# OVERVIEW_GROUP_NAME = "OVERVIEWGroup"
# CONNECTED_GROUP_NAME = "CONNECTEDGroup"
def broadcast(content, group):
    if type(content) is not str:
        # print("notString")
        content = json.dumps(content)
    #print(content)
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            "type": 'new_content',
            "content": content,
        })


#def push_all_data():
#    broadcast(getAllFixturesAndTemplates(False), settings.CONNECTED_GROUP_NAME)
#    broadcast(getAllFixturesAndTemplates(True), settings.OVERVIEW_GROUP_NAME)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add(settings.OVERVIEW_GROUP_NAME, self.channel_name)

        await self.accept()

        await sync_to_async(send_meta_data)()
        await self.send(json.dumps(await sync_to_async(get_template_json)()))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(  # langsam
            settings.OVERVIEW_GROUP_NAME,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            settings.CONNECTED_GROUP_NAME,
            self.channel_name
        )

    async def new_content(self, event):
        await self.send(event['content'])

    async def receive(self, text_data):

        try:
            text_data_json = json.loads(text_data)
            key = list(text_data_json.keys())[0]

            if key == "newFixture":
                await sync_to_async(addFixture)(text_data_json)
            elif key =="editFixture" in text_data:
                await sync_to_async(editFixture)(text_data_json)
            elif key =="deleteFixture" in text_data:
                await sync_to_async(deleteFixture)(text_data_json)
            elif key =="setProject" in text_data:

                if await sync_to_async(setProject)(text_data_json):
                    await self.channel_layer.group_add(settings.CONNECTED_GROUP_NAME,self.channel_name)
                    await self.channel_layer.group_discard(settings.OVERVIEW_GROUP_NAME,self.channel_name)
                    await sync_to_async(update_main_display_project)()
                    await sync_to_async(addPagesIfNotExisting)()
                    await sync_to_async(send_all_project_data)()

            elif key =="deleteProject":
                await self.channel_layer.group_add(
                    settings.OVERVIEW_GROUP_NAME,
                    self.channel_name
                )
                await self.channel_layer.group_discard(
                    settings.CONNECTED_GROUP_NAME,
                    self.channel_name
                )
                await sync_to_async(update_main_display_project)()
                await sync_to_async(deleteProject)(text_data_json)
            elif key == "newProject":
                await sync_to_async(newProject)(text_data_json)
                await sync_to_async(send_meta_data)()
            elif key == "newPage":
                await sync_to_async(newPage)()
                await sync_to_async(update_main_display_max_page)()
            elif key == "deletePage":
                await sync_to_async(deletePage)(text_data_json)
                await sync_to_async(update_main_display_max_page)()
            elif key == "editMixerFader":
                await sync_to_async(editFader)(text_data_json)
            elif key == "editMixerButton":
                await sync_to_async(editButton)(text_data_json)
            elif key == "setMixerColor" :
                await sync_to_async(setMixerColor)(text_data_json)
                await sync_to_async(updateMixerColor)()
            elif key == "addFixtureToGroup":
                await sync_to_async(addFixtureToGroup)(text_data_json)
            elif key == "removeFixtureFromGroup":
                await sync_to_async(removeFixtureFromGroup)(text_data_json)
            elif key == "deleteGroup":
                await sync_to_async(deleteGroup)(text_data_json)
            elif key == "newGroup" :
                await sync_to_async(newGroup)(text_data_json)
            elif key == "selectFixture":
                await sync_to_async(selectFixture)(text_data_json)
            elif key == "deselectFixture":
                await sync_to_async(deselectFixture)(text_data_json)
            elif key == "selectFixtureGroup":
                await sync_to_async(selectGroup)(text_data_json)
            elif key == "deselectFixtureGroup":
                await sync_to_async(deselectGroup)(text_data_json)

            await sync_to_async(updateDisplayText)()

        except ValueError as e:
            print("NO VALID JSON: " + text_data)
            self.disconnect()
            return

class MixerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            settings.MIXER_GROUP_NAME,
            self.channel_name
        )

        await self.accept()
        # 4 Prefix, 2 Display, ... contend
        await sync_to_async(set_mixer_online)("true")
        # await sync_to_async(push_all_data)()
        await sync_to_async(updateDisplayText)()
        await sync_to_async(updateMixerColor)()

    async def disconnect(self, close_code):
        # Leave room group asdasdasd
        await self.channel_layer.group_discard(
            settings.MIXER_GROUP_NAME,
            self.channel_name
        )
        await sync_to_async(set_mixer_online)("false")
        # await sync_to_async(push_all_data)()

    async def new_content(self, event):
        await self.send(event['content'])

    async def receive(self, text_data):
        #print(text_data)

        if text_data == "reqMain":
            await self._update_main_display()
            await self._change_page(0)
            await sync_to_async(update_main_display_max_page)()
        if text_data == "setup":
            project = await sync_to_async(Project.objects.get)(id=await sync_to_async(get_loaded_project)())
            if project.setup == "true":
                project.setup = "false"
                if project.channels_mode == "true":
                    await sync_to_async(broadcast)("infoChannels", MIXER_GROUP_NAME)
                else:
                    await sync_to_async(broadcast)("infoPlaybacks", MIXER_GROUP_NAME)
            else:
                project.setup = "true"
                await sync_to_async(broadcast)("infoSetup", MIXER_GROUP_NAME)
            await sync_to_async(project.save)()
            #await sync_to_async(push_all_data)()
        if text_data == "channel":
            project = await sync_to_async(Project.objects.get)(id=await sync_to_async(get_loaded_project)())
            if project.channels_mode == "true":
                project.channels_mode = "false"
                if project.setup == "false": await sync_to_async(broadcast)("infoPlaybacks", MIXER_GROUP_NAME)
            else:
                project.channels_mode = "true"
                if project.setup == "false": await sync_to_async(broadcast)("infoChannels", MIXER_GROUP_NAME)
            await sync_to_async(project.save)()
            #await sync_to_async(push_all_data)()
            await self._change_page(0)
            await sync_to_async(update_main_display_max_page)()
        elif text_data == "pageUP":
            await self._change_page(1)
        elif text_data == "pageDOWN":
            await self._change_page(-1)

    async def _change_page(self, direction):
        project_id = await sync_to_async(get_loaded_project)()
        project = await sync_to_async(Project.objects.get)(id=project_id)
        mixer = await sync_to_async(lambda: list(project.mixer_set.all()))()
        if project.channels_mode == "true":
            current_mixer_channel_page = int(await sync_to_async(get_mixer_channel_page)())
            fixtures = project.fixture_set.all()
            pages = await sync_to_async(len)(fixtures)
            pages = pages / 5
            if (current_mixer_channel_page > 0 or direction > 0) and (
                    current_mixer_channel_page + 1 < math.ceil(pages) or direction < 0):
                await sync_to_async(set_mixer_channel_page)(current_mixer_channel_page + direction)
            await sync_to_async(update_main_display_page)(current_mixer_channel_page + direction)
        else:
            pages = await sync_to_async(lambda: list(mixer[0].mixerpage_set.all()))()
            current_page = await sync_to_async(get_mixer_page)()
            current_index = next((i for i, p in enumerate(pages) if str(p.id) == str(current_page)), None)
            if direction == 1 and current_index < len(pages) - 1:
                await sync_to_async(set_mixer_page)(pages[current_index + 1].id)
            elif direction == -1 and current_index > 0:
                await sync_to_async(set_mixer_page)(pages[current_index - 1].id)
            await sync_to_async(update_main_display_page)(current_index + direction)
        await sync_to_async(updateDisplayText)()

    async def _update_main_display(self):
        now = datetime.now()
        await self.send("infoConnected")
        await self.send("dclh" + str(now.hour))
        await self.send("dclm" + str(now.minute - 1))
        await sync_to_async(update_main_display_project)()


# MixerHelper
def update_main_display_project():
    try:
        project_id = get_loaded_project()
        project = Project.objects.get(id=project_id)
        projName = project.project_name
        broadcast("proj" + projName, MIXER_GROUP_NAME)
    except:
        broadcast("proj ", MIXER_GROUP_NAME)


def update_main_display_page(page):
    broadcast("page" + str(page + 1), MIXER_GROUP_NAME)


def update_main_display_max_page():
    project_id = get_loaded_project()
    project = Project.objects.get(id=project_id)
    if project.channels_mode == "false":
        print("Channels false")
        mixer = project.mixer_set.all()
        pages = mixer[0].mixerpage_set.all()
        broadcast("mpge" + str(len(pages)), MIXER_GROUP_NAME)
    else:
        fixtures = project.fixture_set.all()
        pages = len(fixtures) / 5
        broadcast("mpge" + str(math.ceil(pages)), MIXER_GROUP_NAME)


def updateDisplayText():
    return
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0]
    if project.channels_mode == "false":
        print("Mixer Modee")
        try:
            mixer_page = mixer.mixerpage_set.all().get(id=get_mixer_page())
        except:
            pages = mixer.mixerpage_set.all()
            set_mixer_page(pages[0].id)
            return
        faders = mixer_page.mixerfader_set.all()
        index = 0
        for fader in faders:
            broadcast(str("disp" + str(index) + fader.name), MIXER_GROUP_NAME)
            hex_color = fader.color.replace("#", "")
            color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            broadcast(
                "mcol" + str(index + 1) + "{:03d}".format(color[0], ) + "{:03d}".format(color[1], ) + "{:03d}".format(
                    color[2], ), MIXER_GROUP_NAME)
            index += 1
    else:

        mixer_channel_page = int(get_mixer_channel_page())
        fixtures = project.fixture_set.all()
        print("Channel Mode" + str(mixer_channel_page))
        for index in range(5):
            if len(fixtures) > index + mixer_channel_page * 5:
                fixture = fixtures[index + mixer_channel_page * 5]
                broadcast(str("disp" + str(index) + fixture.fixture_name), MIXER_GROUP_NAME)
            else:
                broadcast(str("disp" + str(index) + ""), MIXER_GROUP_NAME)
            #hex_color = fader.color.replace("#", "")
            #color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            #broadcast("mcol" + str(index + 1) + "{:03d}".format(color[0], ) + "{:03d}".format(color[1], ) + "{:03d}".format(
            #    color[2], ), MIXER_GROUP_NAME)


def updateMixerColor():
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0].color

    color = tuple(int(mixer[i:i + 2], 16) for i in (0, 2, 4))
    broadcast(str("colr" + str(color[0])), MIXER_GROUP_NAME)
    broadcast(str("colg" + str(color[1])), MIXER_GROUP_NAME)
    broadcast(str("colb" + str(color[2])), MIXER_GROUP_NAME)

def send_all_project_data():
    project = Project.objects.get(id=get_loaded_project())
    broadcast(json.dumps(project.get_fixture_json()), settings.CONNECTED_GROUP_NAME)
    broadcast(json.dumps(project.get_group_json()), settings.CONNECTED_GROUP_NAME)
    broadcast(json.dumps(project.get_mixer_json()), settings.CONNECTED_GROUP_NAME)
    broadcast(json.dumps(get_meta_data()), settings.CONNECTED_GROUP_NAME)





def send_fixture_data():
    project = Project.objects.get(id=get_loaded_project())
    broadcast(json.dumps(project.get_fixture_json()), settings.CONNECTED_GROUP_NAME)

def send_group_data():
    project = Project.objects.get(id=get_loaded_project())
    broadcast(json.dumps(project.get_group_json()), settings.CONNECTED_GROUP_NAME)
def send_mixer_data():
    project = Project.objects.get(id=get_loaded_project())
    broadcast(json.dumps(project.get_mixer_json()), settings.CONNECTED_GROUP_NAME)

def send_meta_data():
    broadcast(json.dumps(get_meta_data()), settings.CONNECTED_GROUP_NAME)
    broadcast(json.dumps(get_meta_data()), settings.OVERVIEW_GROUP_NAME)

