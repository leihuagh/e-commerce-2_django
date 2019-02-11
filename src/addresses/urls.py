from django.conf.urls import url

from .views import (
  checkout_address_create_view,
  CheckoutAddressReuseView,
  AddressListView,
  AddressCreateView,
  AddressUpdateView,
  )

urlpatterns = [
  url(r'^checkout/address/create/$', checkout_address_create_view, name='create'),
  url(r'^checkout/address/reuse/$', CheckoutAddressReuseView.as_view(), name='reuse'),
  url(r'^$', AddressListView.as_view(), name='list'),
  url(r'^create/$', AddressCreateView.as_view(), name='address-create'),
  url(r'^update/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
]

