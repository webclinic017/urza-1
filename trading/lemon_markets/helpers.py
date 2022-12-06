import random, string


def format_currency(amount):
    """
    lemon.markets expects currency in hundreds of cents,
    this function expects amount in Euros and converts to hundreds of cents (rounded)
    """
    return int(amount * 10000)


def create_idempotency(length=4):
    """Create Idempotency Key to avoid multiple requests."""
    ''.join(random.choices(string.ascii_letters + string.digits, k=length))
