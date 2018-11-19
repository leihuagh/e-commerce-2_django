from django.db import models
from django.db.models.signals import post_save

from django.conf import settings

from accounts.models import GuestEmail

# Create your models here.
import stripe
stripe.api_key = 'sk_test_r3EsRHlzW559L1tojcPhYbBd'

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
  def new_or_get(self, request):
    user = request.user
    guest_email_id = request.session.get('guest_email_id')
    obj = None
    created = False
    if user.is_authenticated():
      obj, created = self.model.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
      guset_email_obj = GuestEmail.objects.get(id=guest_email_id)
      obj, created = self.model.objects.get_or_create(email=guset_email_obj.email)
    else:
      pass
    return obj, created

class BillingProfile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True)
  email = models.EmailField()
  active = models.BooleanField(default=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  customer_id = models.CharField(max_length=120, null=True, blank=True)

  def __str__(self):
    return self.email

  objects = BillingProfileManager()


def user_created_receiver(sender, instance, created, *args, **kwargs):
  if created and instance.email:
    BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)