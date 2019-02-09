from django.conf.urls import url

from .views import (
  contact_page,
  )

urlpatterns = [
  url(r'^$', contact_page, name='home'),
]
