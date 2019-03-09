from django.conf.urls import url

from .views import (
  OrderListView,
  OrderDetailView,
  LibraryView,
  VerifyOwnership,
  OrderDetailGeneratePDFView
)


urlpatterns = [
  url(r'^$', OrderListView.as_view(), name='list'),
  url(r'^library/$', LibraryView.as_view(), name='library'),
  url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='detail'),
  url(r'^(?P<order_id>[0-9A-Za-z]+)/download/$', OrderDetailGeneratePDFView.as_view(), name='detail-download'),
  url(r'^endpoint/verify/ownership/$', VerifyOwnership.as_view(), name='verify-ownership'),
]
