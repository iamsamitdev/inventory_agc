from django import views
from django.urls import path
from . import views

urlpatterns = [
    # Frontend
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login, name='login'),

    # Backend
]
