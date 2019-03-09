from django.conf.urls import url

from .views import (
  CartHomeView,
  CartUpdateView,
  CheckoutHomeView,
  CheckoutDoneView
)


urlpatterns = [
  url(r'^$', CartHomeView.as_view(), name='home'),
  url(r'^update/$', CartUpdateView.as_view(), name='update'),
  url(r'^checkout/success/$', CheckoutDoneView.as_view(), name='success'),
  url(r'^checkout/$', CheckoutHomeView.as_view(), name='checkout'),
]
