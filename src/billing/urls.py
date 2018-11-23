from django.conf.urls import url

from .views import (
  payment_method_view,
  payment_method_create_view,
  billing_home
  )

urlpatterns = [
  url(r'^$', billing_home, name='home'),
  url(r'^payment-method/$', payment_method_view, name='payment_method'),
  url(r'^payment-method/create/$', payment_method_create_view, name='create'),
]
