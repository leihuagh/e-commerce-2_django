from django.conf.urls import url

from .views import (
  payment_method_view
  )

urlpatterns = [
  url(r'^payment-method/$', payment_method_view, name='payment_method'),
]

