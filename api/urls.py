from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="apiOverview"),
    path('coinList', views.coin_list, name="coinList"),
    path('marketCap', views.market_cap, name="marketCap"),
]