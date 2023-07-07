from django import views
from django.urls import path
from . import views
# from .views import WebcamCaptureView

urlpatterns = [
    # Frontend
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name='logout'),

    # Backend
    path('backend/dashboard', views.dashboard, name='dashboard'),
    path('backend/product', views.product, name='product'),
    path('backend/product/create', views.create_product, name='create_product'),

    # Chart
    path('backend/chart', views.chart, name='chart'),

    # Video Capture
    path('backend/video', views.capture, name='video'),

]
