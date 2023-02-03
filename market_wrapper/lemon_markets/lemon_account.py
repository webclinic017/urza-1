import json

import requests

from market_wrapper.lemon_markets.utils import format_currency, create_idempotency, get_base_url


class LemonAccountWrapper:
    @staticmethod
    def get_account_info(trading_key, paper):
        try:
            request = requests.get(f"{get_base_url(paper)}account/",
                                   headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error"}
        return request.json()

    @staticmethod
    def withdraw(trading_key, paper, amount, pin):
        try:
            request = requests.post(f"{get_base_url(paper)}account/withdrawals",
                                    data=json.dumps({"amount": format_currency(amount),
                                                     "pin": pin,
                                                     "idempotency": create_idempotency()}),
                                    headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error"}
        return request.json()

    @staticmethod
    def get_withdrawals(trading_key, paper):
        try:
            request = requests.get(f"{get_base_url(paper)}account/withdrawals",
                                   headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error"}
        return request.json()

    @staticmethod
    def get_bank_statements(paper):
        request = requests.get(f"{get_base_url(paper)}account/bankstatements",
                               headers={"Authorization": f"Bearer {key}"})
        return request.json()

    @staticmethod
    def get_documents(paper):
        request = requests.get(f"{get_base_url(paper)}account/documents",
                               headers={"Authorization": f"Bearer {key}"})
        return request.json()

    @staticmethod
    def get_document(paper, document_id):
        request = requests.get(f"{get_base_url(paper)}account/documents/{document_id}",
                               headers={"Authorization": f"Bearer {key}"})
        return request.json()
