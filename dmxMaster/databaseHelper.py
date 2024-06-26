from .models import Settings, Project


def set_loaded_project(projectID):
    projectIDSetting = Settings.objects.get(key="loadedProject")
    projectIDSetting.value = str(projectID)
    projectIDSetting.save()


def get_loaded_project():
    projectIDSetting = Settings.objects.get(key="loadedProject")
    return int(projectIDSetting.value)


def set_mixer_page(mixerpage):
    set_setting("mixerPage", mixerpage)


def get_mixer_page():
    return (get_setting("mixerPage"))


def get_loaded_project():
    projectIDSetting = Settings.objects.get(key="loadedProject")
    return int(projectIDSetting.value)


def set_setting(key, value):
    setting = Settings.objects.get(key=key)
    setting.value = str(value)
    setting.save()


def get_setting(key):
    return Settings.objects.get(key=key).value


# testasd


def set_mixer_online(online):
    mixer_online_setting = Settings.objects.get(key="mixerOnline")
    mixer_online_setting.value = online
    mixer_online_setting.save()
    if online == "false":
        project = Project.objects.get(id=get_loaded_project())
        project.setup = "false"
        project.save()


def get_mixer_online():
    return Settings.objects.get(key="mixerOnline").value

def set_mixer_channel_page(mixerpage):
    set_setting("mixerChannelPage", mixerpage)


def get_mixer_channel_page():
    return (get_setting("mixerChannelPage"))


def set_clipboard(mixerpage):
    set_setting("clipboard", mixerpage)


def get_clipboard():
    return (get_setting("clipboard"))