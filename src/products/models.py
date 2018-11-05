import random
import os
from django.db import models

# Create your models here.

def get_filename_ext(filepath):
  base_name = os.path.basename(filepath)
  name, ext = os.path.splitext(base_name)
  return name, ext


def upload_image_path(instance, filename):
  print(instance)
  print(filename)
  new_filename = random.randint(1, 1000000)
  name, ext = get_filename_ext(filename)
  final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
  return 'products/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)


class ProductManager(models.Manager):
  def featured(self):
    return self.get_queryset().filter(featured=True)

  def get_by_id(self, id):
    qs = self.get_queryset().filter(id=id) # self.get_queryset() == Product.objects
    if qs.count() == 1:
      return qs.first()
    return None

class Product(models.Model):
  title = models.CharField(max_length=120)
  description = models.TextField()
  price = models.DecimalField(decimal_places=2, max_digits=20, default=19.99)
  image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
  featured = models.BooleanField(default=False)


  objects = ProductManager()

  def __str__(self):
    return self.title
  
  # def __unicode__(self): # in python 2
  #   return self.title
