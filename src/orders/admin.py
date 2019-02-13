from django.contrib import admin

from .models import Order, ProductPurchase


class OrderAdmin(admin.ModelAdmin):
  list_display  = ['__str__', 'billing_profile', 'shipping_address_final', 'billing_address_final', 'cart', 'status', 'total', 'active']
  list_display_links = ['__str__']
  list_filter = ['status', 'active']
  search_fields = ['order_id', 'billing_profile__email', 'cart__id']
  ordering = ['-timestamp']
  
  class Meta:
    model = Order


admin.site.register(Order, OrderAdmin)


class ProductPurchaseAdmin(admin.ModelAdmin):
  list_display  = ['__str__', 'order_id', 'billing_profile', 'refunded']
  list_display_links = ['__str__']
  list_filter = ['product', 'order_id', 'billing_profile', 'refunded']
  search_fields = ['order_id', 'product__title', 'billing_profile__email']
  ordering = ['-timestamp']
  
  class Meta:
    model = ProductPurchase
  

admin.site.register(ProductPurchase, ProductPurchaseAdmin)
