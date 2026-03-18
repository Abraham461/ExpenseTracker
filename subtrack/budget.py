from calendar import monthrange
from datetime import date
from decimal import Decimal
from typing import Optional

from django.db.models import Sum
from django.utils import timezone

from .models import UserProfile


def get_budget_context(user, today: Optional[date] = None, profile: Optional[UserProfile] = None) -> dict:
    today = today or timezone.localdate()
    profile = profile or UserProfile.objects.get_or_create(user=user)[0]

    month_start = today.replace(day=1)
    days_in_month = monthrange(today.year, today.month)[1]
    month_end = date(today.year, today.month, days_in_month)

    if profile.budget_start_date and (
        profile.budget_start_date.year != today.year or profile.budget_start_date.month != today.month
    ):
        profile.month_remaining_budget = None
        profile.budget_start_date = None
        profile.save(update_fields=['month_remaining_budget', 'budget_start_date'])

    period_start = month_start
    if profile.budget_start_date and profile.budget_start_date.year == today.year and profile.budget_start_date.month == today.month:
        if profile.budget_start_date > period_start:
            period_start = profile.budget_start_date

    if period_start > today:
        period_start = today

    period_budget = profile.month_remaining_budget or Decimal('0.00')
    has_budget = period_budget > 0
    if not has_budget:
        return {
            'has_budget': False,
            'period_start': period_start,
            'period_budget': period_budget,
            'base_daily_limit': None,
            'allowed_to_date': None,
            'daily_limit': None,
            'remaining_today': None,
            'remaining_period': None,
            'period_total': None,
            'period_total_before_today': None,
            'today_total': None,
        }

    days_in_period = (month_end - period_start).days + 1
    if days_in_period <= 0:
        days_in_period = 1
    days_elapsed = (today - period_start).days + 1
    if days_elapsed <= 0:
        days_elapsed = 1

    base_daily_limit = (period_budget / Decimal(days_in_period)).quantize(Decimal('0.01'))
    allowed_to_date = (base_daily_limit * Decimal(days_elapsed)).quantize(Decimal('0.01'))

    expenses = user.expenses.all()
    period_total = expenses.filter(spent_on__gte=period_start, spent_on__lte=today).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    period_total_before_today = expenses.filter(spent_on__gte=period_start, spent_on__lt=today).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    today_total = expenses.filter(spent_on=today).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    daily_limit = base_daily_limit
    remaining_today = (base_daily_limit - today_total).quantize(Decimal('0.01'))
    remaining_period = (period_budget - period_total).quantize(Decimal('0.01'))

    return {
        'has_budget': True,
        'month_start': month_start,
        'period_start': period_start,
        'month_end': month_end,
        'period_budget': period_budget,
        'days_in_month': days_in_month,
        'days_in_period': days_in_period,
        'days_elapsed': days_elapsed,
        'base_daily_limit': base_daily_limit,
        'allowed_to_date': allowed_to_date,
        'daily_limit': daily_limit,
        'remaining_today': remaining_today,
        'remaining_period': remaining_period,
        'period_total': period_total,
        'period_total_before_today': period_total_before_today,
        'today_total': today_total,
    }
