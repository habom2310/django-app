from django.contrib import admin
from .models import Item

class InventoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['item_name']}),
        ('Buy information', {'fields': ['buy_date', 'buy_price', 'buy_source']}),
        ('Sell information', {'fields': ['sell_date', 'sell_price', 'sell_source']}),
        ('Profit/Loss', {'fields': ['profit_loss']}),
    ]
    # inlines = [ItemInline]
    # list_display = ('item_name', 'buy_price', 'buy_date')

admin.site.register(Item, InventoryAdmin)
