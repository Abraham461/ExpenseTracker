from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subtrack', '0006_remove_userprofile_monthly_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='expenses',
                to='subtrack.category',
            ),
        ),
        migrations.AlterField(
            model_name='expense',
            name='spent_on',
            field=models.DateField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
