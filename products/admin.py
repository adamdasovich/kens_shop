from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'status', 'featured', 'created_at')
    list_filter = ('category', 'status', 'featured', 'created_at')
    search_fields = ('name', 'description', 'materials')
    list_editable = ('status', 'featured')
    ordering = ('-created_at',)
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Status', {
            'fields': ('price', 'status', 'featured')
        }),
        ('Product Details', {
            'fields': ('dimensions', 'materials', 'weight')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order')
    list_filter = ('is_primary', 'product__category')
    list_editable = ('is_primary', 'order')