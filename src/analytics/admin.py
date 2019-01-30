from django.contrib import admin

from .models import ObjectViewed, UserSession

# Register your models here.


admin.site.register(ObjectViewed)


class UserSessionAdmin(admin.ModelAdmin):

  list_display = ['id', '__str__', 'ip_address', 'session_key', 'active', 'ended', 'timestamp']
  list_display_links = ['__str__']
  list_filter = ['active', 'ended']
  search_fields = ['id', 'ip_address', 'session_key']
  ordering = ['-timestamp']

  class Meta:
    model = UserSession


admin.site.register(UserSession, UserSessionAdmin)