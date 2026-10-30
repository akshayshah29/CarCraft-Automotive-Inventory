from django.contrib import admin
from django.utils.html import mark_safe
from .models import Brand, Vehicle, VehicleImage, VehicleWishlist, VehicleEnquiry


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ('image', 'image_preview', 'caption', 'image_url')
    readonly_fields = ('image_preview',)
    verbose_name = "Gallery Image"
    verbose_name_plural = "Vehicle Gallery Images (Upload additional photos here)"

    def image_preview(self, obj):
        if obj and obj.pk and obj.display_image:
            return mark_safe(f'<a href="{obj.display_image}" target="_blank"><img src="{obj.display_image}" style="max-height: 50px; max-width: 90px; border-radius: 4px; object-fit: cover; border: 1px solid #444;" /></a>')
        return mark_safe('<span style="color: #888;">(No image yet)</span>')
    image_preview.short_description = "Preview"


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'image_preview', 'caption', 'image')
    list_filter = ('vehicle__brand', 'vehicle')
    search_fields = ('vehicle__model_name', 'vehicle__brand__name', 'caption')
    readonly_fields = ('image_preview',)
    fields = ('vehicle', 'image', 'image_preview', 'caption', 'image_url')

    def image_preview(self, obj):
        if obj and obj.display_image:
            return mark_safe(f'<a href="{obj.display_image}" target="_blank"><img src="{obj.display_image}" style="max-height: 80px; max-width: 120px; border-radius: 6px; object-fit: cover; border: 1px solid #444;" /></a>')
        return mark_safe('<span style="color: #888;">(No image)</span>')
    image_preview.short_description = "Preview"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'slug', 'logo_preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'country')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj and obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 35px; border-radius: 4px;" />')
        elif obj and obj.logo_url:
            return mark_safe(f'<img src="{obj.logo_url}" style="max-height: 35px; border-radius: 4px;" />')
        return mark_safe('<span style="color: #888;">No Logo</span>')
    logo_preview.short_description = "Logo"


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'year', 'price', 'fuel_type', 'transmission', 'availability', 'is_featured', 'gallery_count')
    list_display_links = ('thumbnail_preview', 'title')
    list_filter = ('brand', 'fuel_type', 'transmission', 'body_type', 'availability', 'is_featured', 'year')
    search_fields = ('model_name', 'brand__name', 'vin', 'description')
    prepopulated_fields = {'slug': ('brand', 'model_name', 'year')}
    list_editable = ('availability', 'is_featured', 'price')
    readonly_fields = ('main_image_preview',)
    inlines = [VehicleImageInline]
    save_on_top = True

    fieldsets = (
        ('Vehicle Identity & Pricing', {
            'fields': (
                ('brand', 'model_name'),
                ('year', 'slug'),
                ('price', 'availability', 'is_featured'),
            )
        }),
        ('Primary Vehicle Photo (Main Display)', {
            'fields': (
                'main_image',
                'main_image_preview',
                'image_url',
            ),
            'description': 'Upload the primary vehicle photo below. It will be used as the hero photo on the vehicle detail page and card previews across the dealership. Additional gallery images can be uploaded in the Gallery Images section below.'
        }),
        ('Technical Specifications', {
            'fields': (
                ('fuel_type', 'transmission', 'body_type'),
                ('mileage', 'engine_capacity', 'horsepower'),
                ('color', 'vin'),
            )
        }),
        ('Vehicle Overview & Features', {
            'fields': (
                'description',
                'features',
            )
        }),
    )

    def thumbnail_preview(self, obj):
        if obj and obj.display_image:
            return mark_safe(f'<img src="{obj.display_image}" style="width: 55px; height: 38px; border-radius: 4px; object-fit: cover;" />')
        return mark_safe('<span style="color: #888;">—</span>')
    thumbnail_preview.short_description = "Photo"

    def main_image_preview(self, obj):
        if obj and obj.display_image:
            return mark_safe(f'<a href="{obj.display_image}" target="_blank"><img src="{obj.display_image}" style="max-height: 140px; border-radius: 6px; object-fit: cover; border: 1px solid #444;" /></a>')
        return mark_safe('<span style="color: #888;">No image uploaded or set</span>')
    main_image_preview.short_description = "Current Main Image Preview"

    def gallery_count(self, obj):
        count = obj.gallery_images.count()
        return f"{count} photos"
    gallery_count.short_description = "Gallery"


@admin.register(VehicleEnquiry)
class VehicleEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle', 'email', 'phone', 'preferred_contact', 'created_at')
    list_filter = ('preferred_contact', 'created_at')
    search_fields = ('name', 'email', 'phone', 'vehicle__model_name')


@admin.register(VehicleWishlist)
class VehicleWishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'created_at')

