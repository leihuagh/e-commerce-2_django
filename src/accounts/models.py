from django.db import models

# Create your models here.

class GuestEmail(models.Model):
  email = models.EmailField()
  active = models.BooleanField(default=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.email