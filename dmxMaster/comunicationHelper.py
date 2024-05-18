from .models import MixerPage, MixerFader
from .models import Template
from .models import Channel
from .models import Fixture, Project, Mixer, Settings
import json
import random



def set_loaded_project(projectID):
    projectIDSetting = Settings.objects.get(key="loadedProject")
    projectIDSetting.value = str(projectID)
    projectIDSetting.save()

def get_loaded_project():
    projectIDSetting = Settings.objects.get(key="loadedProject")
    return int(projectIDSetting.value)




#testasd


def set_mixer_online(online):
    mixer_online_setting = Project.objects.get(key="mixerOnline")
    mixer_online_setting.value = str(online)
    mixer_online_setting.save()


def get_mixer_online():
    return Project.objects.get(key="mixerOnline").value

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

    #global loadedProject
    #loadedProject = project.id


def addPagesIfNotExisting():
    try:
        print(get_loaded_project())
        project = Project.objects.get(id=get_loaded_project())
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
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0]
    pages = mixer.mixerpage_set.all()
    mixer_page = MixerPage(mixer=mixer, pageID=len(pages))  # change to 0 later
    mixer_page.save()
    for number in range(1, 5):
        fader = MixerFader(mixerPage=page, name=str(number), color="ffffff", isTouched="false", value="0",
                           assignedID=-1, assignedType="")
        fader.save()

def deletePage():
    page = MixerPage.objects.get(id=int(json["deletePage"]))
    page.delete()


