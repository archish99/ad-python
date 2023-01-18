from django.contrib import admin
from django.urls import path

# from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('GlobalAjax', views.GlobalAjax, name='GlobalAjax'),
    path('', views.Dashboard, name='home'),
    # url(r'^$', views.base, name='base')
]