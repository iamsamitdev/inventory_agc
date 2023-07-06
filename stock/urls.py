from django import views
from django.urls import path
from . import views

urlpatterns = [
    # Frontend
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),

    # Backend
    path('backend/dashboard', views.dashboard, name='dashboard'),
    path('backend/product', views.product, name='product'),

]
