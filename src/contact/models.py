from django.db import models


class Contact(models.Model):
  fullname = models.CharField(max_length=120)
  email = models.EmailField(blank=True, null=True)
  content = models.TextField(blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.email
