from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'name', 'nickname', 'address_type', 'address_line_1', 'city', 'country', 'state', 'postal_code']
  list_display_links = ['__str__']
  list_filter = ['billing_profile__email', 'address_type', 'city', 'country', 'state']
  search_fields = ['id', 'billing_profile__email', 'address_type', 'city', 'country', 'state']
  ordering = ['-id']

  class Meta:
    model = Address


admin.site.register(Address, AddressAdmin)
