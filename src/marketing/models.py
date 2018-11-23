from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.

User = settings.AUTH_USER_MODEL


class MarketingPreference(models.Model):
  user            = models.OneToOneField(User)
  subscribed      = models.BooleanField(default=True)
  mailchimp_msg   = models.TextField(null=True, blank=True)
  timestamp       = models.DateTimeField(auto_now_add=True)
  update          = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.email




def marketing_pref_update_receiver(sender, instance, created, *args, **kwargs):
  if created:
    pass
    print("Add user to mailchimp")


post_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)




def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
  if created:
    MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=User)