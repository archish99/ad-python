
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup', views.signup, name='signup'),
    path('RegisterFinish', views.RegisterFinish, name='RegisterFinish'),
    path('gAds', views.gAds, name='gAds'),
    # path('RegisterWalletConnect', views.registerWalletconnect, name='RegisterWalletConnect'),
    # path('RegisterFortmatic', views.registerFortmatic, name='RegisterFortmatic'),
    # path('CoinBaseRedrict', views.CoinBaseRedrict, name='CoinBaseRedrict'),
    # url(r'^$', views.base, name='base')
]