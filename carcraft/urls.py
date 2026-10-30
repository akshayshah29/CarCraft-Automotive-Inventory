from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Custom Staff & Dealership Management Dashboard
    path('dashboard/', views.staff_dashboard_view, name='dashboard'),
    path('dashboard/order/<str:order_number>/status/', views.staff_update_order_status, name='staff_update_order'),
    path('dashboard/appointment/<str:appointment_id>/status/', views.staff_update_appointment_status, name='staff_update_appointment'),
    
    # Official Django Admin
    path('admin/', admin.site.urls),

    # Main Project Views
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('search/', views.global_search_view, name='search'),
    path('wishlist/', views.wishlist_view, name='wishlist'),

    # Modular Apps
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cars/', include('vehicles.urls', namespace='vehicles')),
    path('parts/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('services/', include('services.urls', namespace='services')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = 'carcraft.views.handler404'
handler500 = 'carcraft.views.handler500'
