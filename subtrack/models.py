from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_TRIAL = 'trial'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_TRIAL, 'Trial'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    BILLING_MONTHLY = 'monthly'
    BILLING_YEARLY = 'yearly'
    BILLING_WEEKLY = 'weekly'
    BILLING_CUSTOM = 'custom'
    BILLING_CHOICES = [
        (BILLING_MONTHLY, 'Monthly'),
        (BILLING_YEARLY, 'Yearly'),
        (BILLING_WEEKLY, 'Weekly'),
        (BILLING_CUSTOM, 'Custom'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    service_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CHOICES, default=BILLING_MONTHLY)
    billing_date = models.DateField()
    trial_end_date = models.DateField(null=True, blank=True)
    reminder_days_before = models.PositiveSmallIntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['billing_date', 'service_name']

    def __str__(self):
        return self.service_name

    def monthly_cost_equivalent(self) -> Decimal:
        if self.billing_cycle == self.BILLING_YEARLY:
            return (self.amount / Decimal('12')).quantize(Decimal('0.01'))
        if self.billing_cycle == self.BILLING_WEEKLY:
            return (self.amount * Decimal('4.33')).quantize(Decimal('0.01'))
        return self.amount

    def is_due_for_reminder(self, on_date=None) -> bool:
        on_date = on_date or timezone.now().date()
        target_date = self.billing_date - timedelta(days=self.reminder_days_before)
        return self.is_active and self.status != self.STATUS_CANCELLED and on_date == target_date


class Notification(models.Model):
    TYPE_BILLING = 'billing'
    TYPE_TRIAL_END = 'trial_end'
    TYPE_CHOICES = [
        (TYPE_BILLING, 'Billing Reminder'),
        (TYPE_TRIAL_END, 'Trial Ending Reminder'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_BILLING)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)

    class Meta:
        ordering = ['-sent_at']


class SubscriptionUsage(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage_entries')
    month = models.DateField(help_text='Store month as first day of month')
    used = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('subscription', 'month')
        ordering = ['-month']

    def __str__(self):
        return f'{self.subscription.service_name} - {self.month:%Y-%m}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    month_remaining_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Optional: expected budget for the current month.',
    )
    budget_start_date = models.DateField(null=True, blank=True)
    daily_email_reminders = models.BooleanField(
        default=False,
        help_text='Send daily email reminders to log expenses.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} profile'


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
    )
    reason = models.CharField(max_length=200, blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_on = models.DateField(default=timezone.now, db_index=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-spent_on', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.amount} on {self.spent_on:%Y-%m-%d}'


class ExpenseNotification(models.Model):
    TYPE_DAILY = 'daily'
    TYPE_OVERSPEND = 'overspend'
    TYPE_MONTHLY = 'monthly_insight'
    TYPE_CHOICES = [
        (TYPE_DAILY, 'Daily Reminder'),
        (TYPE_OVERSPEND, 'Overspend Alert'),
        (TYPE_MONTHLY, 'Monthly Insight'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expense_notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
