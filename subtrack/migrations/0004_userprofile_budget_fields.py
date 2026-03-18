from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtrack', '0003_remove_expense_category_expense_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='month_remaining_budget',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Optional: remaining budget for the current month.',
                max_digits=12,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='budget_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
