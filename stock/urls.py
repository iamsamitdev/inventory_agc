from django import views
from django.urls import path
from . import views

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
    path('backend/product/<int:product_id>', views.get_product, name='product_detail'),
    path('backend/product/<int:product_id>/update', views.update_product, name='update_product'),
    path('backend/product/<int:product_id>/delete', views.delete_product, name='delete_product'),

    # Chart
    path('backend/chart', views.chart_view, name='chart'),

    # Realtime Streamlit
    path('backend/dashboardrealtime', views.dashboardrealtime, name='dashboardrealtime'),

]
