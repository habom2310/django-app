from django import forms
from .models import Item

class SellForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'buy_price', 'buy_source']
        

