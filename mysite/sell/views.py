from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Item
from django.utils import timezone
from .forms import SellForm
import datetime


class IndexView(generic.ListView):
    template_name = 'sell/index.html'
    context_object_name = 'latest_item_list'

    def get_queryset(self):
        """Return the last five published items"""
        return Item.objects.filter(buy_date__lte=timezone.now()).order_by('-buy_date')[:5]

class DetailView(generic.DetailView):
    model = Item
    template_name = 'sell/detail.html'

    def get_queryset(self):
        return Item.objects.filter(buy_date__lte=timezone.now())

class SellView(generic.DetailView):
    model = Item
    template_name = 'sell/sell.html'

def sell(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
        sell_price = request.POST.get('sell_price')
        if len(sell_price) == 0:
            return render(request, f'sell/sell.html', {
            'item': item,
            'error_message': "You haven't input any sell price",
        })
            # error_message = "You haven't input any sell price"
            # return HttpResponseRedirect(reverse('sell:sell', args=(item.id,)))

    except (KeyError, Item.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, f'sell/details.html', {
            'item': item,
            'error_message': "something wrong",
        })
    else:
        item.profit_loss = float(sell_price) - item.buy_price
        item.sell_price = sell_price
        item.sell_date = timezone.now()
        item.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('sell:index'))

def add(request):
    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.buy_date = timezone.now()
            item.save()
            return HttpResponseRedirect(reverse('sell:index'))
    else:
        form = SellForm()
    return render(request, 'sell/add.html', {'form': form})

from django.db.models import Q
import math
def summary(request):
    query = request.GET.get('q')
    d_res = {}
    if not query:
        object_list = Item.objects.all()
    else:
        d_res['query'] = query
        object_list = Item.objects.filter(
            Q(item_name__icontains=query)
        )

    n_buy = len(object_list)
    total_buy = 0
    n_sell = 0
    total_sell = 0
    total_profit = 0
    total_buy_of_item_sold = 0
    for obj in object_list:
        total_buy += obj.buy_price
        if obj.sell_price != None:
            n_sell += 1
            total_sell += obj.sell_price
            total_buy_of_item_sold += obj.buy_price
            total_profit += obj.profit_loss

    avg_buy_price = total_buy / n_buy
    avg_sell_price = total_sell / n_sell
    avg_profit = total_profit / n_sell
    avg_profit_percent = math.floor(total_profit / total_buy_of_item_sold * 100)

    d_res['n_buy'] = n_buy
    d_res['total_buy'] = total_buy
    d_res['n_sell'] = n_sell
    d_res['total_sell'] = total_sell
    d_res['total_profit'] = total_profit
    d_res['avg_buy_price'] = avg_buy_price
    d_res['avg_sell_price'] = avg_sell_price
    d_res['avg_profit'] = math.floor(avg_profit)
    d_res['avg_profit_percent'] = avg_profit_percent
    
    return render(request, 'sell/summary.html', d_res)