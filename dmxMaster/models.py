from django.db import models
import json

#from dmxMaster.comunicationHelper import get_mixer_online


# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    setup = models.CharField(max_length=200, default="false")
    def __str__(self):
        return self.project_name + " (" + str(self.id) + ")"

    def generateJson(self, loadedProject):
        if loadedProject == self.id:
            json = {
                "name": self.project_name + "(currently open)",
                "internalID": str(self.id)
            }
        else:
            json = {
                "name": self.project_name,
                "internalID": str(self.id)
            }
        return json

    def generateFullJson(self):
        allMixers = self.mixer_set.all()

        projectJson = {"setup" : self.setup, "fixtureTemplates": [], "fixtures": [], "fixtureGroups": [],
                       "mixer": allMixers[0].generateJson(), "project": self.generateJson(0)}

        allFixtures = self.fixture_set.all()

        for x in allFixtures:
            projectJson["fixtures"].append(x.generateJson())

        allGroups = self.group_set.all()

        for x in allGroups:
            projectJson["fixtureGroups"].append(x.generateJson())

        allTemplates = Template.objects.all()

        for x in allTemplates:
            projectJson["fixtureTemplates"].append(x.generateJson())

        return projectJson


class Fixture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    fixture_name = models.CharField(max_length=200)
    fixture_start = models.IntegerField(default=1)

    def __str__(self):
        return self.fixture_name + " (" + str(self.id) + ")"

    def generateJson(self):
        # print("json")
        channels = self.channel_set.all()

        fixtureJson = {
            "name": self.fixture_name,
            "FixtureGroup": "na",
            "internalID": str(self.id),
            "template": "na",
            "startChannel": str(self.fixture_start),
            "channels": [
            ]
        }
        for x in channels:
            fixtureJson["channels"].append({
                "internalID": str(x.id),
                "ChannelType": x.channel_type,
                "ChannelName": x.channel_name,
                "dmxChannel": str(x.channel_location)
            }, )
        return fixtureJson


class Channel(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=200)
    channel_type = models.CharField(max_length=200)
    channel_value = models.IntegerField(default=0)
    channel_location = models.IntegerField(default=0)

    def __str__(self):
        return self.channel_name + " (" + str(self.id) + ")"


class Template(models.Model):
    template_name = models.CharField(max_length=200)

    def generateJson(self):
        # print("json")
        channels = self.templatechannel_set.all()

        fixtureJson = {
            "name": self.template_name,
            "internalID": str(self.id),
            "channels": [
            ]
        }
        for x in channels:
            fixtureJson["channels"].append({
                "internalID": str(x.id),
                "ChannelType": x.channel_type,
                "ChannelName": x.channel_name,
                "dmxChannel": str(x.channel_location)
            }, )
        return fixtureJson

    def __str__(self):
        return self.template_name + " (" + str(self.id) + ")"


class TemplateChannel(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=200)
    channel_type = models.CharField(max_length=200)
    channel_location = models.IntegerField(default=0)

    def __str__(self):
        return self.channel_name + " (" + str(self.id) + ")"


class Group(models.Model):
    group_name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.group_name + " (" + str(self.id) + ")"

    def generateJson(self):
        # print("json--group")
        grouplinks = self.grouplink_set.all()

        json = {
            "name": self.group_name,
            "internalIDs": [],
        }
        for grouplink in grouplinks:
            json["internalIDs"].append(str(grouplink.fixture.id))

        return json


class GroupLink(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.group_name + " --> " + self.fixture.fixture_name


class Mixer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    color = models.CharField(max_length=200)
    mixerUniqueName = models.CharField(max_length=200, default="")
    mixerType = models.CharField(max_length=200)

    def __str__(self):
        return self.project.project_name + " MIXER"

    def generateJson(self):
        print("json--mixer")
        pages = self.mixerpage_set.all()

        json = {
            "color": "#" + self.color,
            "mixerType": self.mixerType,
            "isMixerAvailable": Settings.objects.get(key="mixerOnline").value,
            "pages": [],
        }
        for page in pages:
            json["pages"].append(page.generateJson())

        return json


class MixerPage(models.Model):
    mixer = models.ForeignKey(Mixer, on_delete=models.CASCADE)
    pageID = models.IntegerField(default=0)

    def __str__(self):
        return "(" + str(self.id )+ ") Project: " + self.mixer.project.project_name + " | Page: " + str(self.pageID) + ""

    def generateJson(self):
        # print("json--MixerPage")
        faders = self.mixerfader_set.all()
        buttons = self.mixerbutton_set.all()

        json = {
            "id": str(self.id),
            "num": str(self.pageID),
            "faders": [],
            "buttons": [],
        }
        for button in buttons:
            json["buttons"].append(button.generateJson())

        for fader in faders:
            json["faders"].append(fader.generateJson())
        return json


class MixerButton(models.Model):
    mixerPage = models.ForeignKey(MixerPage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    isPressed = models.CharField(max_length=200)
    assignedID = models.IntegerField(default=0)
    assignedType = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"

    def generateJson(self):
        # print("json--MixerButton")

        json = {
            "id": str(self.id),
            "name": self.name,
            "color": self.color,
            "isPressed": self.isPressed,
            "assignedID": str(self.assignedID),
            "assignedType": self.assignedType,
        }
        return json


class MixerFader(models.Model):
    mixerPage = models.ForeignKey(MixerPage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    isTouched = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    assignedID = models.IntegerField(default=0)
    assignedType = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"

    def generateJson(self):
        # print("json--MixerFader")
        json = {
            "id": str(self.id),
            "name": self.name,
            "color": self.color,
            "isTouched": self.isTouched,
            "value": self.value,
            "assignedID": str(self.assignedID),
            "assignedType": self.assignedType,
        }
        return json

class Settings(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    def __str__(self):
        return self.key + " : " + self.value