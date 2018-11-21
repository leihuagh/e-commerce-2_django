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

  def charge(self, order_obj, card=None):
    return Charge.objects.do(self, order_obj, card)


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




class ChargeManager(models.Manager):
  def do(self, billing_profile, order_obj, card=None):
    card_obj = card
    if card_obj is None:
      cards = billing_profile.card_set.filter(default=True) # card_obj.billing_profile
      if cards.exists():
        card_obj = cards.first()
    if card_obj is None:
      return False, "No cards available"
    c = stripe.Charge.create(
      amount = int(order_obj.total * 100),
      currency = "usd",
      customer =  billing_profile.customer_id,
      source = card_obj.stripe_id,
      metadata={"order_id": order_obj.order_id},
    )
    new_charge_obj = self.model(
      billing_profile = billing_profile,
      stripe_id = c.id,
      paid = c.paid,
      refunded = c.refunded,
      outcome = c.outcome,
      outcome_type = c.outcome['type'],
      seller_message = c.outcome.get('seller_message'),
      risk_level = c.outcome.get('risk_level'),
    )
    new_charge_obj.save()
    return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
  billing_profile = models.ForeignKey(BillingProfile)
  stripe_id = models.CharField(max_length=120)
  paid = models.BooleanField(default=False)
  refunded = models.BooleanField(default=False)
  outcome = models.TextField(null=True, blank=True)
  outcome_type = models.CharField(max_length=120, null=True, blank=True)
  seller_message = models.CharField(max_length=120, null=True, blank=True)
  risk_level = models.CharField(max_length=120, null=True, blank=True)

  def __str__(self):
    return 'billing profile : {}, stripe id : {} , paid : {}, seller message : {}'.format(self.billing_profile, self.stripe_id, self.paid, self.seller_message)

  objects = ChargeManager()