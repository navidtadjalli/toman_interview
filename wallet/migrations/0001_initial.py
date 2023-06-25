# Generated by Django 4.2.2 on 2023-06-25 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=24, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=14, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('wallet', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to='wallet.wallet', verbose_name='Wallet')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
