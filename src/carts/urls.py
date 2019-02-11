from django.conf.urls import url

from .views import (
  CartHomeView,
  CartUpdateView,
  checkout_home,
  CheckoutDoneView
  )

urlpatterns = [
  url(r'^$', CartHomeView.as_view(), name='home'),
  url(r'^update/$', CartUpdateView.as_view(), name='update'),
  url(r'^checkout/success/$', CheckoutDoneView.as_view(), name='success'),
  url(r'^checkout/$', checkout_home, name='checkout'),
]

