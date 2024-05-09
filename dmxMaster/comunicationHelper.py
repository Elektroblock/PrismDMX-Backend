from .models import MixerPage, MixerFader
from .models import Template
from .models import Channel
from .models import Fixture, Project, Mixer
import json
import random

loadedProject = 0
mixerOnline = False



#test


def set_mixer_online(online):
    global mixerOnline
    mixerOnline = online


def get_mixer_online():
    global mixerOnline
    return mixerOnline


def getAllFixturesAndTemplates(newConnection):
    global loadedProject
    packageJson = {"availableProjects": []}

    allProjects = Project.objects.all()

    for x in allProjects:
        packageJson["availableProjects"].append(x.generateJson(loadedProject))

    if loadedProject > 0 and not newConnection:
        project = Project.objects.get(id=loadedProject)
        packageJson.update(project.generateFullJson())
    else:
        packageJson.update({"fixtureTemplates": [], "fixtures": [], "fixtureGroups": [],
                            "mixer": {"color": "#000000", "mixerType": "na", "isMixerAvailable": "false", "pages": []},
                            "project": {"name": "na", "internalID": "na"}})

    return packageJson


def addFixture(json):
    try:
        global loadedProject
        print(loadedProject)
        project = Project.objects.get(id=loadedProject)
        # print(json["id"])
        fixture = Fixture(project=project, fixture_name=json["newFixture"]["fixture"]["name"],
                          fixture_start=json["newFixture"]["fixture"]["startChannel"])

        if int(fixture.fixture_start) < 1:
            fixture.fixture_start = 1
        fixture.save()
        for newChannel in json["newFixture"]["fixture"]["channels"]:
            print(newChannel)
            channel = Channel(fixture=fixture, channel_name=newChannel["ChannelName"],
                              channel_type=newChannel["ChannelType"], channel_location=newChannel["dmxChannel"])
            channel.save()
    except:
        return


def editFixture(json):
    # print(json["id"])

    try:
        fixture = Fixture.objects.get(id=int(json["editFixture"]["fixture"]["internalID"]))

        fixture.fixture_name = json["editFixture"]["fixture"]["name"]
        fixture.fixture_start = json["editFixture"]["fixture"]["startChannel"]
        if int(fixture.fixture_start) < 1:
            fixture.fixture_start = 1

        fixture.save()
        for newChannel in json["editFixture"]["fixture"]["channels"]:
            print(newChannel)
            channel = Channel.objects.get(id=int(newChannel["internalID"]))
            channel.channel_name = newChannel["ChannelName"]
            channel.channel_location = newChannel["dmxChannel"]
            channel.channel_type = newChannel["ChannelType"]

            channel.save()
    except:
        return


def deleteFixture(json):
    fixture = Fixture.objects.get(id=int(json["deleteFixture"]["internalID"]))
    fixture.delete()


def setProject(json):
    try:
        project = Project.objects.get(id=int(json["setProject"]["project"]["internalID"]))
        global loadedProject
        print(loadedProject)
        loadedProject = int(json["setProject"]["project"]["internalID"])
        print(loadedProject)
        return True
    except:
        return False


def deleteProject(json):
    try:
        global loadedProject
        project = Project.objects.get(id=int(json["deleteProject"]["project"]["internalID"]))
        project.delete()
        if loadedProject == int(json["deleteProject"]["project"]["internalID"]):
            loadedProject = 0
    except:
        return


def newProject(json):
    # r = lambda: random.randint(0, 255)ddd
    # print('#%02X%02X%02X' % (r(), r(), r()))
    project = Project(project_name=json["newProject"]["project"]["name"])
    project.save()
    mixer = Mixer(project=project, color="ffffff", mixerUniqueName="mainMixer", mixerType="5")  # change to 0 later
    mixer.save()

    #global loadedProject
    #loadedProject = project.id


def addPagesIfNotExisting():
    try:

        global loadedProject
        print(loadedProject)
        project = Project.objects.get(id=loadedProject)
    except:
        print("Error")
        return
    mixer = project.mixer_set.all()[0]
    pages = mixer.mixerpage_set.all()
    if len(pages) == 0:
        mixer_page = MixerPage(mixer=mixer, pageID=0)  # change to 0 later
        mixer_page.save()
        for number in range(1, 6):
            print("asd")
            fader = MixerFader(mixerPage=mixer_page, name=str(number), color="ffffff", isTouched="false", value="0",
                               assignedID=-1, assignedType="")
            fader.save()



def newPage():
    global loadedProject
    project = Project.objects.get(id=loadedProject)
    mixer = project.mixer_set.all()[0]
    pages = mixer.mixerpage_set.all()
    mixer_page = MixerPage(mixer=mixer, pageID=len(pages))  # change to 0 later
    mixer_page.save()
    for number in range(1, 5):
        fader = MixerFader(mixerPage=page, name=str(number), color="ffffff", isTouched="false", value="0",
                           assignedID=-1, assignedType="")
        fader.save()
