from django.conf.urls import url

from .views import (
  CartHomeView,
  cart_update,
  checkout_home,
  CheckoutDoneView
  )

urlpatterns = [
  url(r'^$', CartHomeView.as_view(), name='home'),
  url(r'^update/$', cart_update, name='update'),
  url(r'^checkout/success/$', CheckoutDoneView.as_view(), name='success'),
  url(r'^checkout/$', checkout_home, name='checkout'),
]

