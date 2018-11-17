from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import GuestEmail

from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.

User = get_user_model()


# class UserAdmin(admin.ModelAdmin):
#   search_fields = ['email']

#   class Meta:
#     model = User

class UserAdmin(BaseUserAdmin):
  form = UserAdminChangeForm
  add_form = UserAdminCreationForm

  list_display = ('email', 'full_name', 'admin', 'staff', 'active')
  list_filter = ('admin', 'staff', 'active', 'email')
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info and Full Name', {'fields': ('full_name', 'last_login', )}),
    ('Permissions', {'fields': ('admin', 'staff', 'active')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'full_name', 'password1', 'password2')}
    ),
  )
  search_fields = ('email', 'full_name', )
  ordering = ('email', )
  filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)



class GuestEmailAdmin(admin.ModelAdmin):
  search_fields = ['email']
  class Meta:
    model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)