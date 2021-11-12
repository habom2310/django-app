from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Item
from django.utils import timezone
from .forms import SellForm

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

