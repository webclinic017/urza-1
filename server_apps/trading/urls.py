from django.urls import path

from server_apps.trading import views

app_name = "trading"
urlpatterns = [
    path(r"quote/", views.get_quote, name="quote")
]
