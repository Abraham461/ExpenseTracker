from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from subtrack.budget import get_budget_context
from subtrack.insights import get_monthly_insights
from subtrack.models import ExpenseNotification, UserProfile


class Command(BaseCommand):
    help = 'Send daily expense reminders and overspend alerts.'

    def handle(self, *args, **options):
        today = date.today()
        daily_count = 0
        overspend_count = 0
        monthly_count = 0

        for profile in UserProfile.objects.select_related('user'):
            user = profile.user
            if not user.email:
                continue

            if profile.daily_email_reminders and not ExpenseNotification.objects.filter(
                user=user, notification_type=ExpenseNotification.TYPE_DAILY, sent_at__date=today
            ).exists():
                message = f'Reminder: log your expenses for {today:%Y-%m-%d} in SubTrack.'
                send_mail(
                    subject='Daily Expense Reminder',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=settings.EMAIL_FAIL_SILENTLY,
                )
                ExpenseNotification.objects.create(
                    user=user, notification_type=ExpenseNotification.TYPE_DAILY, message=message
                )
                daily_count += 1

            budget = get_budget_context(user, today=today, profile=profile)
            if (
                budget['has_budget']
                and budget['period_total'] > budget['allowed_to_date']
                and not ExpenseNotification.objects.filter(
                    user=user, notification_type=ExpenseNotification.TYPE_OVERSPEND, sent_at__date=today
                ).exists()
            ):
                message = (
                    f'Alert: You have spent {settings.CURRENCY_PREFIX}{budget["period_total"]} '
                    f'so far this month (since {budget["period_start"]}), '
                    f'which is above your allowed {settings.CURRENCY_PREFIX}{budget["allowed_to_date"]} '
                    f'as of today.'
                )
                send_mail(
                    subject='Overspending Alert',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=settings.EMAIL_FAIL_SILENTLY,
                )
                ExpenseNotification.objects.create(
                    user=user, notification_type=ExpenseNotification.TYPE_OVERSPEND, message=message
                )
                overspend_count += 1

            if today.day == 1 and not ExpenseNotification.objects.filter(
                user=user, notification_type=ExpenseNotification.TYPE_MONTHLY, sent_at__date=today
            ).exists():
                prev_month = today.replace(day=1) - timedelta(days=1)
                insights = get_monthly_insights(user, year=prev_month.year, month=prev_month.month)

                top_reason = 'None'
                if insights['common_reasons']:
                    top_reason = insights['common_reasons'][0]['reason'] or 'Unspecified'

                highest_day_line = 'None'
                if insights['highest_spend_day']:
                    highest_day_line = (
                        f"{insights['highest_spend_day']['spent_on']}: "
                        f"{settings.CURRENCY_PREFIX}{insights['highest_spend_day']['total']}"
                    )

                largest_expense_line = 'None'
                if insights['highest_expense']:
                    largest_expense_line = (
                        f"{settings.CURRENCY_PREFIX}{insights['highest_expense'].amount} "
                        f"on {insights['highest_expense'].spent_on}"
                    )

                change_line = f"{settings.CURRENCY_PREFIX}{insights['change_amount']}"
                if insights['change_percent'] is not None:
                    change_line = (
                        f"{settings.CURRENCY_PREFIX}{insights['change_amount']} "
                        f"({insights['change_percent']}%)"
                    )

                message = (
                    f"Monthly Insights for {insights['month_start']:%B %Y}:\n"
                    f"- Total spent: {settings.CURRENCY_PREFIX}{insights['month_total']}\n"
                    f"- Top reason: {top_reason}\n"
                    f"- Highest spending day: {highest_day_line}\n"
                    f"- Largest expense: {largest_expense_line}\n"
                    f"- Change vs last month: {change_line}\n\n"
                    "Log in to SubTrack and open Insights for the full breakdown."
                )

                send_mail(
                    subject=f"Your {insights['month_start']:%B %Y} Spending Insights",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=settings.EMAIL_FAIL_SILENTLY,
                )
                ExpenseNotification.objects.create(
                    user=user, notification_type=ExpenseNotification.TYPE_MONTHLY, message=message
                )
                monthly_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Sent {daily_count} daily reminder(s), {overspend_count} overspend alert(s), '
                f'and {monthly_count} monthly insight(s).'
            )
        )
