from datetime import datetime

import pytest
from django.urls import reverse

from news.models import Article
import pytest
from channels.testing import WebsocketCommunicator

from urza.asgi import application


@pytest.mark.django_db
def test_create_article():
    for i in range(10):
        Article.objects.create(url=f"example.com/{i}", date_time=datetime.now(), headline="Example",
                               html="<html></html>")
    assert Article.objects.count() == 10


@pytest.mark.django_db
def test_most_recent(client):
    for i in range(2):
        Article.objects.create(url=f"example.com/{i}", date_time=datetime(year=1970, month=2, day=2),
                               headline="Example",
                               html="<html></html>")
    url = reverse("news:most-recent")
    response = client.get(url)
    assert response.status_code == 200

    article_list = response.json()["articles"]
    assert isinstance(article_list, list)
    assert isinstance(article_list[0], dict)
    assert article_list[0]["url"] == "example.com/0"
    assert article_list[1]["url"] == "example.com/1"
    assert article_list[0]["headline"] == "Example"
    assert article_list[0]["date_time"] == datetime(year=1970, month=2, day=2).isoformat() + "Z"
    assert article_list[0]["html"] == "<html></html>"


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
class TestTradingWebsocket:
    async def test_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application=application, path="/ws/news/")
        connected, _ = await communicator.connect()
        assert connected

        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/ws/news/'
        )
        await communicator.connect()
        await communicator.send_json_to({"data": "test"})
        response = await communicator.receive_json_from()
        assert response == {"data": "test"}
        await communicator.disconnect()
