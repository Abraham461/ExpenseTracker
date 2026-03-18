from django.contrib import admin

from .models import (
    Category,
    Expense,
    ExpenseNotification,
    Notification,
    Subscription,
    SubscriptionUsage,
    UserProfile,
)

admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(Notification)
admin.site.register(SubscriptionUsage)
admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(ExpenseNotification)
