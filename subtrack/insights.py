from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal

from typing import Optional

from django.db.models import Count, Sum
from django.utils import timezone


def _month_bounds(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    end = date(year, month, monthrange(year, month)[1])
    return start, end


def get_monthly_insights(user, year: Optional[int] = None, month: Optional[int] = None) -> dict:
    today = timezone.localdate()
    year = year or today.year
    month = month or today.month

    start, end = _month_bounds(year, month)
    expenses = user.expenses.filter(spent_on__gte=start, spent_on__lte=end)
    month_total = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    common_reasons = (
        expenses.values('reason')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total', '-count')[:5]
    )

    daily_totals = expenses.values('spent_on').annotate(total=Sum('amount')).order_by('-total')
    days_logged = expenses.values('spent_on').distinct().count()
    highest_spend_day = daily_totals.first()

    highest_expense = expenses.order_by('-amount', '-spent_on', '-created_at').first()

    previous_month_end = start - timedelta(days=1)
    prev_start, prev_end = _month_bounds(previous_month_end.year, previous_month_end.month)
    prev_total = (
        user.expenses.filter(spent_on__gte=prev_start, spent_on__lte=prev_end).aggregate(total=Sum('amount'))[
            'total'
        ]
        or Decimal('0.00')
    )

    change_amount = (month_total - prev_total).quantize(Decimal('0.01'))
    change_percent = None
    if prev_total > 0:
        change_percent = (change_amount / prev_total * Decimal('100')).quantize(Decimal('0.1'))

    return {
        'month_start': start,
        'month_end': end,
        'month_total': month_total.quantize(Decimal('0.01')),
        'prev_month_total': prev_total.quantize(Decimal('0.01')),
        'change_amount': change_amount,
        'change_percent': change_percent,
        'common_reasons': common_reasons,
        'highest_spend_day': highest_spend_day,
        'highest_expense': highest_expense,
        'has_expenses': expenses.exists(),
        'days_logged': days_logged,
    }
