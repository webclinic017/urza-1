from django.urls import path

from trading import views

app_name = "trading"
urlpatterns = [
    path(r"info/", views.get_account_info, name="info"),
    path(r"withdraw/<int:amount>/", views.withdraw, name="info"),
    path(r"withdrawals/", views.withdrawals, name="info"),
    path(r"bank_statements/", views.bank_statements, name="info"),
    path(r"documents/", views.documents, name="info"),
    path(r"document/", views.document, name="info")
]
