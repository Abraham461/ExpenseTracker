from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('subtrack', '0006_remove_userprofile_monthly_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='daily_email_reminders',
            field=models.BooleanField(default=False, help_text='Send daily email reminders to log expenses.'),
        ),
    ]
