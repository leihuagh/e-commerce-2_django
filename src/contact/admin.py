from django.contrib import admin

from .models import Contact

# Register your models here.


class ContactAdmin(admin.ModelAdmin):

  list_display  = ['email', 'fullname', 'timestamp']
  list_display_links = ['email']
  list_filter = ['email']
  search_fields = ['id', 'email']
  ordering = ['-timestamp']
  
  class Meta:
    model = Contact


admin.site.register(Contact, ContactAdmin)