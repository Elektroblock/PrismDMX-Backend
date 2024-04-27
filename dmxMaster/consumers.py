# chat/consumers.py
import json

import channels.layers
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.conf import settings
from .models import Fixture, Template


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



        self.send('')

    def disconnect(self, close_code):
        # Leave room group asdasdasd
        self.channel_layer.group_discard(
            settings.MAIN_GROUP_NAME,
            self.channel_name
        )

    def new_content(self, event):
        self.send(event['content'])

    def receive(self, text_data):

        if "test" == text_data:
            self.send('{"fixtures":[{"internalID":"0","name":"LampeRGB-1","FixtureGroup":"1","startChannel":"12","channels":[{"internalID":"0","ChanneltType":"RED","ChannelType":"RED","dmxChannel":"0"},{"internalID":"1","ChanneltType":"GREEN","ChannelType":"GREEN","dmxChannel":"1"},{"internalID":"2","ChanneltType":"BLUE","ChannelType":"BLUE","dmxChannel":"3"}]}],"fixtureTemplates":[{"internalID":"0","name":"LampeRGB","channels":[{"internalID":"0","ChanneltType":"RED","ChannelType":"RED","dmxChannel":"0"},{"internalID":"1","ChanneltType":"GREEN","ChannelType":"GREEN","dmxChannel":"1"},{"internalID":"2","ChanneltType":"BLUE","ChannelType":"BLUE","dmxChannel":"2"}]}]}')
            return

        if "test2" == text_data:

            allDataJson ={
            "fixtureTemplates": [],"fixtures": []}

            allFixtures = Fixture.objects.all()

            for x in allFixtures:
                allDataJson["fixtures"].append(x.generateJson())

            allTemplates = Template.objects.all()

            for x in allTemplates:
                allDataJson["fixtureTemplates"].append(x.generateJson())

            self.send(json.dumps(allDataJson))
            return


        try:
            text_data_json = json.loads(text_data)
        except ValueError as e:
            self.send("NO VALID JSON")
            return


        broadcast_content(text_data_json)
