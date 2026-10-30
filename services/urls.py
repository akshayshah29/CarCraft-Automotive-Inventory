from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list_view, name='list'),
    path('book/', views.book_service_view, name='book'),
    path('book/<slug:slug>/', views.book_service_view, name='book_specific'),
    path('detail/<slug:slug>/', views.service_detail_view, name='detail'),
    path('confirmation/<str:appointment_id>/', views.appointment_confirmation_view, name='confirmation'),
    path('history/', views.appointment_history_view, name='history'),
    path('cancel/<str:appointment_id>/', views.cancel_appointment_view, name='cancel'),
]
