from django.db import models

from django.conf import settings
from products.models import Product

# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
  def new(self, user=None):
    user_obj = None
    if user is not None:
      if user.is_authenticated():
        user_obj = user
    return self.model.objects.create(user=user_obj)


class Cart(models.Model):
  user = models.ForeignKey(User, null=True, blank=True)
  products = models.ManyToManyField(Product, blank=True)
  total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = CartManager()

  def __str__(self):
    return str(self.id)