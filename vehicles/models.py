from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
        ('Dual-Clutch', 'Dual-Clutch Automatic'),
    ]

    BODY_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
    ]

    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Sold', 'Sold'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='vehicles')
    model_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Automatic')
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES, default='Sedan')
    mileage = models.PositiveIntegerField(help_text="Odometer reading in kilometers")
    engine_capacity = models.CharField(max_length=100, help_text="e.g. 2.0L Turbocharged I4")
    horsepower = models.PositiveIntegerField(help_text="Horsepower rating (HP)", default=200)
    color = models.CharField(max_length=50, default='Graphite Grey')
    vin = models.CharField(max_length=17, unique=True, help_text="17-character Vehicle Identification Number")
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')
    is_featured = models.BooleanField(default=False)
    
    # Image support: uploaded image or direct external CDN URL (Unsplash luxury automotive)
    main_image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="High-resolution image URL")
    
    description = models.TextField()
    features = models.TextField(help_text="Comma or newline-separated key vehicle features")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name}-{self.model_name}-{self.year}")
            unique_slug = base_slug
            num = 1
            while Vehicle.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def title(self):
        return f"{self.brand.name} {self.model_name}"

    @property
    def display_image(self):
        if self.main_image:
            try:
                return self.main_image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        first_gallery = self.gallery_images.first()
        if first_gallery:
            return first_gallery.display_image
        return 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80'

    @property
    def features_list(self):
        if not self.features:
            return []
        items = [f.strip() for f in self.features.replace('\n', ',').split(',') if f.strip()]
        return items

    def __str__(self):
        return f"{self.year} {self.brand.name} {self.model_name}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='vehicles/gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)

    @property
    def display_image(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return self.vehicle.display_image

    def __str__(self):
        return f"Gallery image for {self.vehicle.title}"


class VehicleWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_wishlist')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vehicle')

    def __str__(self):
        return f"{self.user.username} saved {self.vehicle.title}"


class VehicleEnquiry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    message = models.TextField()
    preferred_contact = models.CharField(max_length=20, default='Phone', choices=[('Phone', 'Phone'), ('Email', 'Email'), ('WhatsApp', 'WhatsApp')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Enquiry from {self.name} for {self.vehicle.title}"
