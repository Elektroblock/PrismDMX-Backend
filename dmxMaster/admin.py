from django.contrib import admin

# Register your models here.
from .models import TemplateChannel, Settings, Template, Channel, Fixture, Group, GroupLink, MixerFader, MixerPage, \
    MixerButton, Mixer, Project, SelectedFixture, SelectedGroup

admin.site.register(TemplateChannel)
admin.site.register(Template)
admin.site.register(Channel)
admin.site.register(Fixture)
admin.site.register(Group)
admin.site.register(GroupLink)
admin.site.register(MixerFader)
admin.site.register(MixerPage)
admin.site.register(MixerButton)
admin.site.register(Mixer)
admin.site.register(Project)
admin.site.register(Settings)
admin.site.register(SelectedFixture)
admin.site.register(SelectedGroup)