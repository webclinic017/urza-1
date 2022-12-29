from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/news/", consumers.NewsConsumer.as_asgi(), name="ws-news"),
]
