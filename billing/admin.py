from django.contrib import admin

from .models import (
  BillingProfile,
  Card,
  Charge
)


class BillingProfileAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'user', 'customer_id', 'active', 'timestamp', 'updated']
  list_display_links = ['__str__']
  list_filter = ['email', 'user', 'active']
  search_fields = ['id', 'email', 'user__email', 'customer_id']
  ordering = ['-timestamp']

  class Meta:
    model = BillingProfile


admin.site.register(BillingProfile, BillingProfileAdmin)


class CardAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'billing_profile', 'stripe_id', 'brand', 'country', 'exp_month', 'exp_year', 'last4', 'default', 'active', 'timestamp', 'updated']
  list_display_links = ['__str__']
  list_filter = ['billing_profile__email', 'brand', 'country', 'exp_month', 'exp_year', 'last4', 'default', 'active']
  search_fields = ['id', 'billing_profile__email', 'stripe_id', 'country', 'last4']
  ordering = ['-timestamp']

  class Meta:
    model = Card


admin.site.register(Card, CardAdmin)


class ChargeAdmin(admin.ModelAdmin):
  list_display = ['id', 'billing_profile', 'stripe_id', 'paid', 'refunded', 'outcome_type', 'seller_message', 'risk_level']
  list_display_links = ['billing_profile']
  list_filter = ['paid', 'refunded', 'outcome_type', 'seller_message', 'risk_level']
  search_fields = ['id', 'billing_profile__email', 'stripe_id']
  ordering = ['-id']

  class Meta:
    model = Charge

admin.site.register(Charge, ChargeAdmin)
