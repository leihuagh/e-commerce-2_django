from django.contrib import admin

from .models import (
  ObjectViewed,
  UserSession
)


class ObjectViewedAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'content_type', 'object_id', 'content_object', 'ip_address', 'timestamp']
  list_display_links = ['__str__']
  list_filter = ['user', 'object_id']
  search_fields = ['id','user__email', 'object_id']
  ordering = ['-timestamp']

  class Meta:
    model = ObjectViewed


admin.site.register(ObjectViewed, ObjectViewedAdmin)


class UserSessionAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'ip_address', 'session_key', 'active', 'ended', 'timestamp']
  list_display_links = ['__str__']
  list_filter = ['active', 'ended']
  search_fields = ['id', 'ip_address', 'session_key']
  ordering = ['-timestamp']

  class Meta:
    model = UserSession


admin.site.register(UserSession, UserSessionAdmin)
