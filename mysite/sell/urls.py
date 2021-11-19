from django.urls import path

from . import views

app_name = 'sell'
urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('add/', views.add, name='add'),
    path('<int:pk>/sell/', views.SellView.as_view(), name='sell'),
    path('<int:item_id>/sell/confirm_sell', views.sell, name='confirm_sell'),
    path('summary/', views.summary, name='summary')
]