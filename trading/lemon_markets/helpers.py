import random, string


def format_currency(amount):
    """
    lemon.markets expects currency in hundreds of cents,
    this function expects amount in Euros and converts to hundreds of cents (rounded)
    """
    return int(amount * 10000)


def create_idempotency(length=4):
    """Create idempotency key to avoid multiple requests."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def concat_ISINs(ISINs):
    """Concat ISINs for multi-result request"""
    if isinstance(ISINs, str):
        return ISINs
    return ",".join(isin for isin in ISINs)
