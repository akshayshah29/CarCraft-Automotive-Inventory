from django.contrib import admin
from .models import Service, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_featured')
    search_fields = ('name', 'description')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'customer_name', 'service', 'vehicle_model', 'preferred_date', 'preferred_time', 'status')
    list_filter = ('status', 'service', 'preferred_date')
    search_fields = ('appointment_id', 'customer_name', 'customer_email', 'customer_phone', 'vehicle_model')
    list_editable = ('status',)
