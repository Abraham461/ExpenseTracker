from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['name'], 'unique_together': {('user', 'name')}},
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_cycle', models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('weekly', 'Weekly'), ('custom', 'Custom')], default='monthly', max_length=20)),
                ('billing_date', models.DateField()),
                ('trial_end_date', models.DateField(blank=True, null=True)),
                ('reminder_days_before', models.PositiveSmallIntegerField(default=3)),
                ('status', models.CharField(choices=[('active', 'Active'), ('trial', 'Trial'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='subtrack.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['billing_date', 'service_name']},
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('billing', 'Billing Reminder'), ('trial_end', 'Trial Ending Reminder')], default='billing', max_length=20)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=255)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='subtrack.subscription')),
            ],
            options={'ordering': ['-sent_at']},
        ),
        migrations.CreateModel(
            name='SubscriptionUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text='Store month as first day of month')),
                ('used', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usage_entries', to='subtrack.subscription')),
            ],
            options={'ordering': ['-month'], 'unique_together': {('subscription', 'month')}},
        ),
    ]
