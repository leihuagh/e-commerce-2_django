from django.conf.urls import url

from .views import (
  cart_home,
)


urlpatterns = [
  url(r'^$', cart_home, name='home'),
]
