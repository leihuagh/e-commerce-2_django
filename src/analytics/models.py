from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
  user            = models.ForeignKey(User, blank=True, null=True)
  content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
  object_id       = models.PositiveIntegerField()
  content_object  = GenericForeignKey('content_type', 'object_id')
  ip_address      = models.CharField(max_length=220, blank=True, null=True)
  timestamp       = models.DateTimeField(auto_now_add=True)

  def __str__(self, ):
    return "%s viewed on: %s" %(self.content_object, self.timestamp)

  class Meta:
    ordering = ['-timestamp']
    verbose_name = 'Object Viewed'
    verbose_name_plural = 'Objects Viewed'