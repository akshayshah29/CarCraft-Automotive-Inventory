import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Service(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    tagline = models.CharField(max_length=200, help_text="Short engaging hook")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Starting estimated price")
    duration = models.CharField(max_length=50, help_text="e.g. 2 - 3 Hours, 45 Minutes")
    icon_class = models.CharField(max_length=50, default='bi-wrench-adjustable', help_text="Bootstrap Icons class name")
    
    # Image support: uploaded image or external URL
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    what_is_included = models.TextField(help_text="Newline separated list of inclusions")
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1613214149922-f1809c99b414?auto=format&fit=crop&w=1000&q=80'

    @property
    def inclusions_list(self):
        if not self.what_is_included:
            return []
        return [inc.strip() for inc in self.what_is_included.split('\n') if inc.strip()]

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    TIME_SLOTS = [
        ('09:00 AM - 11:00 AM', '09:00 AM - 11:00 AM'),
        ('11:00 AM - 01:00 PM', '11:00 AM - 01:00 PM'),
        ('02:00 PM - 04:00 PM', '02:00 PM - 04:00 PM'),
        ('04:00 PM - 06:00 PM', '04:00 PM - 06:00 PM'),
    ]

    appointment_id = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    
    # Vehicle details for service
    vehicle_model = models.CharField(max_length=150, help_text="e.g. 2022 BMW 330i")
    vehicle_reg_number = models.CharField(max_length=50, blank=True, null=True, help_text="License plate number")
    
    # Schedule
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, choices=TIME_SLOTS, default='09:00 AM - 11:00 AM')
    
    # Contact info
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True, help_text="Specific issues, noises, or requests")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-preferred_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"SRV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment #{self.appointment_id} - {self.service.name} for {self.customer_name}"
