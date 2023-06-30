from django.conf.urls import url

from .consumers import ChatConsumer, ChessConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    url(r'^ws/onlinegame/(?P<room_name>\w+)/$', ChessConsumer.as_asgi()),
]