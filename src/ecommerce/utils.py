import random
import string
import os
from django.utils.text import slugify

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
  if new_slug is not None:
    slug = new_slug
  else:
    slug = slugify(instance.title)

  Klass = instance.__class__
  qs_exists = Klass.objects.filter(slug=slug).exists()
  if qs_exists:
    new_slug = "{slug}-{randstr}".format(
      slug=slug,
      randstr=random_string_generator(size=4)
    )
    return unique_slug_generator(instance, new_slug=new_slug)
  return slug


def unique_order_id_generator(instance):
  order_new_id = random_string_generator()

  Klass = instance.__class__
  qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
  if qs_exists:
    
    return unique_order_id_generator(instance)
  return order_new_id


def unique_key_generator(instance):
  size = random.randint(30, 45)
  key = random_string_generator(size=size)

  Klass = instance.__class__
  qs_exists = Klass.objects.filter(key=key).exists()
  if qs_exists:
    return unique_slug_generator(instance)
  return key


def get_filename(path):
  return os.path.basename(path)


def render_to_pdf(template_src, context_dict={}):
  template = get_template(template_src)
  html  = template.render(context_dict)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
  # response = HttpResponse(content_type='application/pdf') 
  # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
  # pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
  if not pdf.err:
    return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return response
  return None