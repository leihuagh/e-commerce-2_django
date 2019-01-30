from django.contrib import admin

# Register your models here.

from .models import Product

class ProductAdmin(admin.ModelAdmin):

  list_display = ['id', '__str__', 'slug', 'price', 'image', 'featured', 'active', 'is_digital', 'timestamp']
  list_display_links = ['__str__']
  list_editable = ['price']
  list_filter = ['featured', 'active', 'is_digital']
  search_fields = ['id', 'title', 'price']
  ordering = ['-timestamp']

  class Meta:
    model = Product


admin.site.register(Product, ProductAdmin)