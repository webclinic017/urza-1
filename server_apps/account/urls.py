from django.urls import path

from server_apps.account import views

app_name = "account"
urlpatterns = [
    path(r"info/", views.get_account_info, name="info"),
    path(r"withdraw/<int:amount>/", views.withdraw, name="info"),
    path(r"withdrawals/", views.get_withdrawals, name="info"),
    path(r"bank_statements/", views.get_bank_statements, name="info"),
    path(r"documents/", views.get_documents, name="info"),
    path(r"document/", views.get_document, name="info")
]
