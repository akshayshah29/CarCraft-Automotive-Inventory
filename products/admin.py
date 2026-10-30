from django.contrib import admin
from .models import ProductCategory, Product, ProductWishlist


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'stock', 'is_featured', 'part_number')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'part_number', 'brand_compatibility', 'description')
    list_editable = ('price', 'stock', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductWishlist)
class ProductWishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
