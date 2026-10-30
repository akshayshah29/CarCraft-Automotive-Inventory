from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list_view, name='list'),
    path('<slug:slug>/', views.vehicle_detail_view, name='detail'),
    path('wishlist/toggle/<int:vehicle_id>/', views.toggle_vehicle_wishlist_view, name='wishlist_toggle'),
]
