

from .models import TemplateChannel
from .models import Template
from .models import Channel
from .models import Fixture, Project
import json


loadedProject = 0

def getAllFixturesAndTemplates():
    packageJson = {"availableProjects": []}

    allProjects = Project.objects.all()

    for x in allProjects:
        packageJson["availableProjects"].append(x.generateJson())

    if (loadedProject>0):
        project = Project.objects.get(id=1)
        packageJson.update(project.generateFullJson())
    else:
        packageJson.update({"fixtureTemplates": [], "fixtures": [], "fixtureGroups": [], "mixer": {"color": "#000000","mixerType": "n/a","isMixerAvailable": "false","pages": []}, "project": {"name": "n/a", "internalID": "n/a"}})

    return packageJson


def addFixture(json):
    # print(json["id"])
    fixture = Fixture(fixture_name=json["newFixture"]["fixture"]["name"], fixture_start=json["newFixture"]["fixture"]["startChannel"])

    fixture.save()
    for newChannel in json["newFixture"]["fixture"]["channels"]:
        print(newChannel)
        channel = Channel(fixture=fixture, channel_name=newChannel["ChannelName"], channel_type=newChannel["ChannelType"], channel_location=newChannel["dmxChannel"])
        channel.save()

def editFixture(json):
    # print(json["id"])
    fixture = Fixture.objects.get(id=int(json["editFixture"]["fixture"]["internalID"]))

    fixture.fixture_name = json["editFixture"]["fixture"]["name"]
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

def setProject(json):
    global loadedProject
    loadedProject = int(json["setProject"]["internalID"])
