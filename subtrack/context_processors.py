from django.conf import settings


def currency(request):
    return {
        'currency_symbol': getattr(settings, 'CURRENCY_SYMBOL', 'MMK'),
        'currency_prefix': getattr(settings, 'CURRENCY_PREFIX', 'MMK '),
    }
