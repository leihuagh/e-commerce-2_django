from django.contrib import admin

from .models import BillingProfile, Card

# Register your models here.

admin.site.register(BillingProfile)
admin.site.register(Card)