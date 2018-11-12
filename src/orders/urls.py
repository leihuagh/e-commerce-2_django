from django.conf.urls import url

from .views import (
  order_home
  )

urlpatterns = [
  url(r'^$', order_home, name='home'),
]

