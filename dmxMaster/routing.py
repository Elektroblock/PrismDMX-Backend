from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/main", consumers.ChatConsumer.as_asgi()),
    re_path("ws/mixer", consumers.MixerConsumer.as_asgi()),
]