from django.contrib import admin

from .models import Cart


class CartAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'user', 'subtotal', 'total', 'timestamp']
  list_display_links = ['__str__']
  list_filter = ['user__email']
  search_fields = ['id', 'user__email']
  ordering = ['-timestamp']

  class Meta:
    model = Cart


admin.site.register(Cart, CartAdmin)
