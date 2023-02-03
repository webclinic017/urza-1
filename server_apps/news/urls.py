from django.urls import path

from server_apps.news import views

app_name = "news"
urlpatterns = [
    path(r"most-recent", views.most_recent, name="most-recent"),
    path(r"most-recent/<int:n>", views.most_recent, name="most-recent"),
]
