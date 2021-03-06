# Generated by Django 3.2.9 on 2021-11-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('buy_price', models.FloatField(verbose_name='buy price')),
                ('buy_date', models.DateTimeField(verbose_name='buy date')),
                ('buy_source', models.CharField(choices=[('EB', 'Ebay'), ('FB', 'Facebook'), ('GT', 'Gumtree'), ('CCV', 'CashConverter'), ('OTHER', 'Other')], default='EB', max_length=10)),
                ('sell_price', models.FloatField(blank=True, null=True, verbose_name='sell price')),
                ('sell_date', models.DateTimeField(blank=True, null=True, verbose_name='sell date')),
                ('sell_source', models.CharField(blank=True, choices=[('EB', 'Ebay'), ('FB', 'Facebook'), ('GT', 'Gumtree'), ('CCV', 'CashConverter'), ('OTHER', 'Other')], max_length=10)),
                ('profit_loss', models.FloatField(default=0, verbose_name='profit/loss')),
            ],
        ),
    ]
