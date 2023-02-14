from django.urls import path

from news import views

app_name = "news"
urlpatterns = [
    path(r"most-recent/", views.most_recent, name="most-recent"),
    path(r"most-recent/<int:n>/", views.most_recent, name="most-recent"),
]
