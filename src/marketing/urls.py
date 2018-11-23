from django.conf.urls import url

from .views import (
  marketing_home
  )

urlpatterns = [
  url(r'^$', marketing_home, name='home'),
]

