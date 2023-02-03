from datetime import datetime

import pytest
from django.urls import reverse

from server_apps.news.models import Article


@pytest.mark.django_db
def test_user_create():
    for i in range(10):
        Article.objects.create(url=f"example.com/{i}", date_time=datetime.now(), headline="Example",
                               html="<html></html>")
    assert Article.objects.count() == 10


@pytest.mark.django_db
def test_view(client):
    url = reverse("news:most-recent")
    response = client.get(url)
    assert response.status_code == 200
