from django.db import models

from carts.models import Cart

# Create your models here.

ORDER_STATUS_CHOICES = (
  ('created', 'Created'),
  ('paid', 'Paid'),
  ('shipped', 'Shipped'),
  ('refunded', 'Refunded'),
)

class Order(models.Model):
  order_id = models.CharField(max_length=120, blank=True)
  cart = models.ForeignKey(Cart)
  status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
  shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
  total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.order_id
  
  