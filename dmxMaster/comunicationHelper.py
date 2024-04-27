

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

