from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtrack', '0005_alter_expensenotification_notification_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='monthly_income',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='month_remaining_budget',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Optional: expected budget for the current month.',
                max_digits=12,
                null=True,
            ),
        ),
    ]
