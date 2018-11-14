from django.conf.urls import url

from .views import (
  checkout_address_create_view,

  )

urlpatterns = [
  url(r'^create/$', checkout_address_create_view, name='create'),

]

