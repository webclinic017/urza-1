from django.urls import path

from server_apps.news import views

app_name = "market"
urlpatterns = [
    path(r"most_recent/", views.most_recent, name="quote"),
]
