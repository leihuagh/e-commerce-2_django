from django.db import models
from django.db.models.signals import post_save, pre_save

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


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
  if not instance.customer_id and instance.email:
    customer = stripe.Customer.create(
      email=instance.email
    )
    instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)







class CardManager(models.Manager):
  def add_new(self, billing_profile, stripe_card_response):
    obj = None
    created = False
    if str(stripe_card_response.object) == 'card':
      new_card = self.model(
        billing_profile=billing_profile,
        stripe_id=stripe_card_response.id,
        brand=stripe_card_response.brand,
        country=stripe_card_response.country,
        exp_month=stripe_card_response.exp_month,
        exp_year=stripe_card_response.exp_year,
        last4=stripe_card_response.last4,
      )
      new_card.save()
      return new_card
    return None



class Card(models.Model):
  billing_profile = models.ForeignKey(BillingProfile)
  stripe_id = models.CharField(max_length=120)
  brand = models.CharField(max_length=120, null=True, blank=True)
  country = models.CharField(max_length=20, null=True, blank=True)
  exp_month = models.IntegerField(null=True, blank=True)
  exp_year = models.IntegerField(null=True, blank=True)
  last4 = models.CharField(max_length=4, null=True, blank=True)
  default = models.BooleanField(default=True)

  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return 'stripe id : {} , {}, {}'.format(self.stripe_id, self.brand, self.last4)

  objects = CardManager()