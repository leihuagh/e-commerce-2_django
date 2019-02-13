from django.contrib import admin

from .models import (
  Product,
  ProductFile
)


class ProductFileInline(admin.TabularInline):
  model = ProductFile
  extra = 1


admin.site.register(ProductFile)


class ProductAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'slug', 'price', 'image', 'featured', 'active', 'is_digital', 'timestamp']
  list_display_links = ['__str__']
  list_editable = ['price']
  list_filter = ['featured', 'active', 'is_digital']
  search_fields = ['id', 'title', 'price']
  ordering = ['-timestamp']
  inlines = [ProductFileInline]

  class Meta:
    model = Product


admin.site.register(Product, ProductAdmin)
