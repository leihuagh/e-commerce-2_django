from django.conf.urls import url

from .views import (
  PaymentMethodView,
  PaymentMethodCreateView,
  billing_home
  )

urlpatterns = [
  url(r'^$', billing_home, name='home'),
  url(r'^payment-method/$', PaymentMethodView.as_view(), name='payment_method'),
  url(r'^payment-method/create/$', PaymentMethodCreateView.as_view(), name='create'),
]
