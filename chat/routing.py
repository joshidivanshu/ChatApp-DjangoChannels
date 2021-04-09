from django.urls import re_path
from . import consumers, consumers2



websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/users/(?P<room_name>\w+)/$', consumers2.StatusConsumer.as_asgi()),
]