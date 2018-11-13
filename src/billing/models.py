from django.db import models
from django.db.models.signals import post_save

from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
  user = models.ForeignKey(User, unique=True, null=True, blank=True)
  email = models.EmailField()
  active = models.BooleanField(default=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
  if created:
    BillingProfile.objects.get_or_create(user=instance)

post_save.connect(user_created_receiver, sender=User)