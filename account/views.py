from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from market_wrapper.account_wrapper import AccountWrapper


@login_required
def get_account_info(request):
    return JsonResponse(AccountWrapper.get_account_info())


@login_required
def withdraw(request, amount):
    return JsonResponse(AccountWrapper.withdraw())


@login_required
def withdrawals(request):
    return JsonResponse(AccountWrapper.get_withdrawals())


@login_required
def bank_statements(request):
    return JsonResponse(AccountWrapper.get_bank_statements())


@login_required
def documents(request):
    return JsonResponse(AccountWrapper.get_documents())


@login_required
def document(request):
    return JsonResponse(AccountWrapper.get_document())
