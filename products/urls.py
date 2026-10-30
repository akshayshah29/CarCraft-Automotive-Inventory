from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_product_wishlist_view, name='wishlist_toggle'),
]
