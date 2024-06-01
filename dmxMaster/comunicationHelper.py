from .models import MixerPage, MixerFader, MixerButton, GroupLink, Group
from .models import Template
from .models import Channel
from .models import Fixture, Project, Mixer, Settings
import json
import random
from dmxMaster.databaseHelper import set_loaded_project, get_loaded_project, set_mixer_page, get_mixer_page, \
    get_loaded_project, set_setting, get_setting, set_mixer_online, get_mixer_online


def get_meta_data(newConnection=False):
    packageJson = {"availableProjects": []}

    allProjects = Project.objects.all()

    for x in allProjects:
        packageJson["availableProjects"].append(x.get_project_json(get_loaded_project()))

    if get_loaded_project() > 0 and not newConnection: #and not newConnection:
        try:
            project = Project.objects.get(id=get_loaded_project())
            packageJson.update({"setup": project.setup, "channels": project.channels_mode, "currentProject" : project.get_project_json(get_loaded_project())})
        except:
            packageJson.update({"setup": "false", "channels": "false"})
            return packageJson
    else:
        packageJson.update({"setup": "false", "channels": "false"})

    #else:
    #    packageJson.update({"fixtureTemplates": [], "fixtures": [], "fixtureGroups": [],
    #                        "mixer": {"color": "#000000", "mixerType": "na", "isMixerAvailable": "false", "pages": []},
    #                        "project": {"name": "na", "internalID": "na"}, "setup": "false", "channels": "false", "selectedFixtureIDs": [], "selectedFixtureGroupIDs": []})

    return packageJson

def get_template_json():
    allTemplates = Template.objects.all()
    all_template_json = []
    for x in allTemplates:
        all_template_json.append(x.generateJson())

    return list(all_template_json)


def addFixture(json):
    try:

        #print(get_loaded_project())
        project = Project.objects.get(id=get_loaded_project())
        # print(json["id"])
        fixture = Fixture(project=project, fixture_name=json["newFixture"]["fixture"]["name"],
                          fixture_start=json["newFixture"]["fixture"]["startChannel"])

        if int(fixture.fixture_start) < 1:
            fixture.fixture_start = 1
        fixture.save()
        for newChannel in json["newFixture"]["fixture"]["channels"]:
           # print(newChannel)
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
        fixture.selected = "false"
        if int(fixture.fixture_start) < 1:
            fixture.fixture_start = 1

        fixture.save()
        for newChannel in json["editFixture"]["fixture"]["channels"]:
            #print(newChannel)
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
        project = Project.objects.get(id=int(json["setProject"]))
        #print(get_loaded_project())
        set_loaded_project(int(json["setProject"]))
        #print(get_loaded_project())
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
    project = Project(project_name=json["newProject"])
    project.save()
    mixer = Mixer(project=project, color="ffffff", mixerUniqueName="mainMixer", mixerType="5")  # change to 0 later
    mixer.save()

    # global loadedProject
    # loadedProject = project.id


def addPagesIfNotExisting():  # also set active Page to first page
    try:
       # print(get_loaded_project())
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
            #print("asd")
            fader = MixerFader(mixerPage=mixer_page, name=str(number), color="ffffff", isTouched="false", value="0",
                               assignedID=-1, assignedType="")
            fader.save()
            button = MixerButton(mixerPage=mixer_page, name=str(number), color="ffffff", isPressed="false",
                                 assignedID=-1,
                                 assignedType="")
            button.save()

    pages = mixer.mixerpage_set.all()
    set_mixer_page(pages[0].id)


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
        button = MixerButton(mixerPage=mixer_page, name=str(number), color="ffffff", isPressed="false", assignedID=-1,
                             assignedType="")
        button.save()


def editFader(json):
    fader = MixerFader.objects.get(id=int(json["editMixerFader"]["fader"]["id"]))
    fader.name = json["editMixerFader"]["fader"]["name"]
    fader.color = json["editMixerFader"]["fader"]["color"]
    fader.assignedType = str(json["editMixerFader"]["fader"]["assignedType"]).replace("#", "")
    fader.assignedID = int(json["editMixerFader"]["fader"]["assignedID"])
    fader.save()

def editButton(json):
    button = MixerButton.objects.get(id=int(json["editMixerButton"]["button"]["id"]))
    button.name = json["editMixerButton"]["button"]["name"]
    button.color = json["editMixerButton"]["button"]["color"]
    button.assignedType = str(json["editMixerButton"]["button"]["assignedType"]).replace("#", "")
    button.assignedID = int(json["editMixerButton"]["button"]["assignedID"])
    button.save()


def deletePage(json_data):
    #print()
    try:
        page = MixerPage.objects.get(id=int(json_data["deletePage"]))
        page.delete()
        if json_data["deletePage"] == get_mixer_page():
            project = Project.objects.get(id=get_loaded_project())
            mixer = project.mixer_set.all()[0]
            pages = mixer.mixerpage_set.all()
            set_mixer_page(pages[0].id)
    except:
        return


def setMixerColor(json_data):
    #print(json_data)
    project = Project.objects.get(id=get_loaded_project())
    mixer = project.mixer_set.all()[0]
    mixer.color = json_data["setMixerColor"].replace("#", "")
    mixer.save()

def addFixtureToGroup(json_data):
    group = Group.objects.get(id=int(json_data["addFixtureToGroup"]["groupID"]))
    fixture = Fixture.objects.get(id=int(json_data["addFixtureToGroup"]["fixtureID"]))
    if not GroupLink.objects.filter(group=group, fixture=fixture).exists():
        group_link = GroupLink(group=group, fixture=fixture)
        group_link.save()

def removeFixtureFromGroup(json_data):
    group = Group.objects.get(id=int(json_data["removeFixtureFromGroup"]["groupID"]))
    fixture = Fixture.objects.get(id=int(json_data["removeFixtureFromGroup"]["fixtureID"]))
    group_link = GroupLink.objects.get(group=group, fixture=fixture)
    group_link.delete()

def newGroup(json_data):
    #print(json_data["newGroup"]["groupName"])
    project = Project.objects.get(id=get_loaded_project())
    group = Group(group_name=json_data["newGroup"]["groupName"], project=project)
    group.save()
def deleteGroup(json_data):
    group = Group.objects.get(id=int(json_data["deleteGroup"]["groupID"]))
    group.delete()

def selectFixture(json_data):

    project = Project.objects.get(id=get_loaded_project())
    fixture = Fixture.objects.get(id=int(json_data["selectFixture"]["fixtureID"]))
    if not SelectedFixture.objects.filter(project=project, fixture=fixture).exists():
        selectedfixture = SelectedFixture(project=project, fixture=fixture)
        selectedfixture.save()

def deselectFixture(json_data):
    try:
        project = Project.objects.get(id=get_loaded_project())
        fixture = Fixture.objects.get(id=int(json_data["deselectFixture"]["fixtureID"]))
        selectedfixture = SelectedFixture.objects.get(project=project, fixture=fixture)
        selectedfixture.delete()
    except:
        return

def selectGroup(json_data):

    project = Project.objects.get(id=get_loaded_project())
    group = Group.objects.get(id=int(json_data["selectFixtureGroup"]["groupID"]))
    group_links = group.grouplink_set.all()
    selectedgroup = SelectedGroup(project=project, group=group)
    selectedgroup.save()
    for group_link in group_links:
        fixture = group_link.fixture
        if not SelectedFixture.objects.filter(project=project, fixture=fixture).exists():
            selectedfixture = SelectedFixture(project=project, fixture=fixture)
            selectedfixture.save()

def deselectGroup(json_data):

    project = Project.objects.get(id=get_loaded_project())
    group = Group.objects.get(id=int(json_data["deselectFixtureGroup"]["groupID"]))
    group_links = group.grouplink_set.all()
    selectedgroup = SelectedGroup.objects.get(project=project, group=group)
    selectedgroup.delete()

    for group_link in group_links:
        fixture = group_link.fixture
        if SelectedFixture.objects.filter(project=project, fixture=fixture).exists():
            selectedfixture = SelectedFixture.objects.get(project=project, fixture=fixture)
            selectedfixture.delete()

