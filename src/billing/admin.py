from django.contrib import admin

from .models import BillingProfile, Card, Charge

# Register your models here.


class BillingProfileAdmin(admin.ModelAdmin):

  list_display = ['id', '__str__', 'user', 'customer_id', 'active', 'timestamp', 'updated']
  list_display_links = ['__str__']
  list_filter = ['email', 'user', 'active']
  search_fields = ['id', 'email', 'user__email', 'customer_id']
  ordering = ['-timestamp']

  class Meta:
    model = BillingProfile


admin.site.register(BillingProfile, BillingProfileAdmin)


admin.site.register(Card)
admin.site.register(Charge)