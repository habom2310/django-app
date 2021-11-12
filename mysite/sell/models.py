from django.db import models
from django.utils import timezone

class Item(models.Model):
    class Source(models.TextChoices):
        EB = "EB", "Ebay"
        FB = "FB", "Facebook"
        GT = "GT", "Gumtree"
        CCV = "CCV", "CashConverter"
        OTHER = "OTHER", "Other"

    item_name = models.CharField(max_length=200)

    def __str__(self):
        return self.item_name

    buy_price = models.FloatField('buy price')
    buy_date = models.DateTimeField('buy date', default=timezone.now)
    buy_source = models.CharField(max_length=10, choices=Source.choices, default=Source.EB)

    sell_price = models.FloatField('sell price', null=True, blank=True)
    sell_date = models.DateTimeField('sell date', null=True, blank=True)
    sell_source = models.CharField(max_length=10, choices=Source.choices, blank=True)

    profit_loss = models.FloatField('profit/loss', null=False, default=0, blank=False)