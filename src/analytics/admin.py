from django.contrib import admin

from .models import ObjectViewed, UserSession

# Register your models here.


admin.site.register(ObjectViewed)
admin.site.register(UserSession)