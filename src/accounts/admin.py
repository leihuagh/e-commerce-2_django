from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import GuestEmail, EmailActivation
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
  form = UserAdminChangeForm
  add_form = UserAdminCreationForm

  list_display = ['id', 'email', 'full_name', 'last_login', 'admin', 'staff', 'is_active', 'timestamp']
  list_display_links = ['email']
  list_filter = ['admin', 'staff', 'is_active', 'email']
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info and Full Name', {'fields': ('full_name', 'last_login', )}),
    ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'full_name', 'password1', 'password2')}
    ),
  )
  search_fields = ['id', 'email', 'full_name', ]
  ordering = ['-timestamp']
  filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class EmailActivationAdmin(admin.ModelAdmin):
  list_display = ['id', 'email', 'key', 'activated', 'forced_expired', 'expires', 'timestamp', 'updated']
  list_display_links = ['email']
  list_filter = ['activated', 'forced_expired', 'expires']
  search_fields = ['id', 'email', 'key']
  ordering = ['-timestamp']
  
  class Meta:
    model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'active', 'timestamp', 'updated']
  list_display_links = ['__str__']
  list_filter = ['active']
  search_fields = ['id', 'email']
  ordering = ['-timestamp']
  
  class Meta:
    model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)
