from .models import MixerPage, MixerFader
from .models import Template
from .models import Channel
from .models import Fixture, Project, Mixer, Settings
import json
import random
from dmxMaster.databaseHelper import set_loaded_project, get_loaded_project, set_mixer_page, get_mixer_page, \
    get_loaded_project, set_setting, get_setting, set_mixer_online, get_mixer_online


def getAllFixturesAndTemplates(newConnection):
    packageJson = {"availableProjects": []}

    allProjects = Project.objects.all()

    for x in allProjects:
        packageJson["availableProjects"].append(x.generateJson(get_loaded_project()))

    if get_loaded_project() > 0 and not newConnection:
        project = Project.objects.get(id=get_loaded_project())
        packageJson.update(project.generateFullJson())
    else:
        packageJson.update({"fixtureTemplates": [], "fixtures": [], "fixtureGroups": [],
                            "mixer": {"color": "#000000", "mixerType": "na", "isMixerAvailable": "false", "pages": []},
                            "project": {"name": "na", "internalID": "na"}})

    return packageJson


def addFixture(json):
    try:
        print(get_loaded_project())
        project = Project.objects.get(id=get_loaded_project())
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
        print(get_loaded_project())
        set_loaded_project(int(json["setProject"]["project"]["internalID"]))
        print(get_loaded_project())
        return True
    except:
        return False


def deleteProject(json):
    try:
        project = Project.objects.get(id=int(json["deleteProject"]["project"]["internalID"]))
        project.delete()
        if get_loaded_project() == int(json["deleteProject"]["project"]["internalID"]):
            set_loaded_project(0)
    except:
        return


def newProject(json):
    # r = lambda: random.randint(0, 255)ddd
    # print('#%02X%02X%02X' % (r(), r(), r()))
    project = Project(project_name=json["newProject"]["project"]["name"])
    project.save()
    mixer = Mixer(project=project, color="ffffff", mixerUniqueName="mainMixer", mixerType="5")  # change to 0 later
    mixer.save()

    # global loadedProject
    # loadedProject = project.id


def addPagesIfNotExisting(): # also set active Page to first page
    try:
        print(get_loaded_project())
        project = Project.objects.get(id=get_loaded_project())
    except:
        print("Error")
        return
    mixer = project.mixer_set.all()[0]
    pages = mixer.mixerpage_set.all()
    set_mixer_page(pages[0].id)
    if len(pages) == 0:
        mixer_page = MixerPage(mixer=mixer, pageID=0)  # change to 0 later
        mixer_page.save()
        for number in range(1, 6):
            print("asd")
            fader = MixerFader(mixerPage=mixer_page, name=str(number), color="ffffff", isTouched="false", value="0",
                               assignedID=-1, assignedType="")
            fader.save()


def newPage():
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0]
    pages = mixer.mixerpage_set.all()
    mixer_page = MixerPage(mixer=mixer, pageID=len(pages))  # change to 0 later
    mixer_page.save()
    for number in range(1, 6):
        fader = MixerFader(mixerPage=mixer_page, name=str(number), color="ffffff", isTouched="false", value="0",
                           assignedID=-1, assignedType="")
        fader.save()


def editFader(json):
    fader = MixerFader.objects.get(id=int(json["editMixerFader"]["fader"]["id"]))
    fader.name = json["editMixerFader"]["fader"]["name"]
    fader.color = json["editMixerFader"]["fader"]["color"]
    fader.assignedType = str(json["editMixerFader"]["fader"]["assignedType"]).replace("#", "")
    fader.assignedID = int(json["editMixerFader"]["fader"]["assignedID"])
    fader.save()


def deletePage(json_data):
    print(json_data)
    page = MixerPage.objects.get(id=int(json_data["deletePage"]))
    page.delete()

def setMixerColor(json_data):
    print(json_data)
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0]
    mixer.color = json_data["setMixerColor"].replace("#","")
    mixer.save()
