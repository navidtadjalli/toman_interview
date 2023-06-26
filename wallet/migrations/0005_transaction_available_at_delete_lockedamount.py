# Generated by Django 4.2.2 on 2023-06-25 23:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_lockedamount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='available_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Available at'),
        ),
        migrations.DeleteModel(
            name='LockedAmount',
        ),
    ]