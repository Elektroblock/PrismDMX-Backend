from django.db import models
import json

# Create your models here.
class Fixture(models.Model):
    fixture_name = models.CharField(max_length=200)
    fixture_start = models.IntegerField()
    fixture_group = models.CharField(max_length=200)

    def __str__(self):
        return self.fixture_name

    def generateJson(self):
        print("json")
        channels = self.channel_set.all()

        fixtureJson = {
            "name": self.fixture_name,
            "FixtureGroup": self.fixture_group,
            "internalID": str(self.id),
            "template": "1",
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
                },)
        return fixtureJson


class Channel(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=200)
    channel_type = models.CharField(max_length=200)
    channel_value = models.IntegerField(default=0)
    channel_location = models.IntegerField(default=0)

    def __str__(self):
        return self.channel_name


class Template(models.Model):
    template_name = models.CharField(max_length=200)

    def generateJson(self):
        print("json")
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
                },)
        return fixtureJson

    def __str__(self):
        return self.template_name


class TemplateChannel(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=200)
    channel_type = models.CharField(max_length=200)
    channel_location = models.IntegerField(default=0)

    def __str__(self):
        return self.channel_name


