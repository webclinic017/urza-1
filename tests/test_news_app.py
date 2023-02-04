import uuid
from datetime import datetime

import pytest
from channels.testing import WebsocketCommunicator
from django.urls import reverse

from news.models import Article
from urza.asgi import application


@pytest.fixture
def test_password():
    return "test-pwd"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.mark.django_db
def test_create_articles():
    for i in range(5):
        Article.objects.create(url=f"example.com/{i}", date_time=datetime(year=1970, month=1, day=1),
                               headline="Example",
                               html="<html></html>")
    assert Article.objects.count() == 5


@pytest.mark.django_db
def test_most_recent(client, create_user, test_password):
    for i in range(10):
        Article.objects.create(url=f"example.com/{i}", date_time=datetime(year=1970, month=2, day=2),
                               headline="Example",
                               html="<html></html>")
    user = create_user()
    url = reverse("news:most-recent")
    client.login(
        username=user.username, password=test_password
    )
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
