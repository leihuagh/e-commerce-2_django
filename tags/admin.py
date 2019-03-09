from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
  list_display  = ['id', '__str__', 'slug', 'active', 'timestamp']
  list_display_links = ['__str__']
  list_filter = ['title', 'active']
  search_fields = ['id', 'title']
  ordering = ['-timestamp']
  
  class Meta:
    model = Tag


admin.site.register(Tag, TagAdmin)
