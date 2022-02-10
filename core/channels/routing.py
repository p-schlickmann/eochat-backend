from django.conf.urls import url
from django.urls import re_path

from core.channels import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_code>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
