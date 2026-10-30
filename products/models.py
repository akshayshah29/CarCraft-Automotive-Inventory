from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    part_number = models.CharField(max_length=50, blank=True, help_text="OEM or Aftermarket Part Number")
    brand_compatibility = models.CharField(max_length=200, default='Universal / Multi-Brand')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)
    
    # Image support: uploaded image or external URL
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    description = models.TextField()
    specifications = models.TextField(blank=True, help_text="Key specifications, materials, warranty")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            while Product.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.main_image:
            return self.main_image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80'

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def specs_list(self):
        if not self.specifications:
            return []
        return [s.strip() for s in self.specifications.split('\n') if s.strip()]

    def __str__(self):
        return self.name


class ProductWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"
