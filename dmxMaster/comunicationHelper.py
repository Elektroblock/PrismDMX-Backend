

from .models import TemplateChannel
from .models import Template
from .models import Channel
from .models import Fixture
import json

def getAllFixturesAndTemplates():
    allDataJson ={"fixtureTemplates": [],"fixtures": []}

    allFixtures = Fixture.objects.all()

    for x in allFixtures:
        allDataJson["fixtures"].append(x.generateJson())

    allTemplates = Template.objects.all()

    for x in allTemplates:
        allDataJson["fixtureTemplates"].append(x.generateJson())

    return allDataJson


def addFixture(json):
    # print(json["id"])
    fixture = Fixture(fixture_name=json["newFixture"]["fixture"]["name"], fixture_start=json["newFixture"]["fixture"]["startChannel"], fixture_group=json["newFixture"]["fixture"]["FixtureGroup"])

    fixture.save()
    for newChannel in json["newFixture"]["fixture"]["channels"]:
        print(newChannel)
        channel = Channel(fixture=fixture, channel_name=newChannel["ChannelName"], channel_type=newChannel["ChannelType"], channel_location=newChannel["dmxChannel"])
        channel.save()

def editFixture(json):
    # print(json["id"])
    fixture = Fixture.objects.get(id=int(json["editFixture"]["fixture"]["internalID"]))

    fixture.fixture_name = json["editFixture"]["fixture"]["name"]
    fixture.fixture_group = json["editFixture"]["fixture"]["FixtureGroup"]
    fixture.fixture_start = json["editFixture"]["fixture"]["startChannel"]

    fixture.save()
    for newChannel in json["editFixture"]["fixture"]["channels"]:
        print(newChannel)
        channel = Channel.objects.get(id=int(newChannel["internalID"]))
        channel.channel_name = newChannel["ChannelName"]
        channel.channel_location = newChannel["dmxChannel"]
        channel.channel_type = newChannel["ChannelType"]

        channel.save()

def deleteFixture(json):
    fixture = Fixture.objects.get(id=int(json["deleteFixture"]["internalID"]))
    fixture.delete()