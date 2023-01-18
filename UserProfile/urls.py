from django.urls import path, include
from . import views
urlpatterns = [
    path('Myprofile', views.Myprofile, name='Myprofile'),
]