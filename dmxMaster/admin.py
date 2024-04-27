from django.contrib import admin

# Register your models here.
from .models import TemplateChannel
from .models import Template
from .models import Channel
from .models import Fixture

admin.site.register(TemplateChannel)
admin.site.register(Template)
admin.site.register(Channel)
admin.site.register(Fixture)