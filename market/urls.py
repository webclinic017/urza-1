from django.urls import path

from market import views

app_name = "market"
urlpatterns = [
    path(r"quote/<str:symbols_or_isins>", views.get_quote, name="quote"),
    path(r"ohlc/<str:symbols_or_isins>/<str:start_date>/<str:frequency>", views.get_ohlc_data, name="ohlc"),
]
