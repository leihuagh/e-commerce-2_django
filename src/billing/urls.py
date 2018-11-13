from django.conf.urls import url

from .views import (
  billing_home
  )

urlpatterns = [
  url(r'^$', billing_home, name='home'),
]

