from django.conf.urls import url

from .views import (
  SalesView,
  SalesAjaxView
)

urlpatterns = [
  url(r'^sales/$', SalesView.as_view(), name='sales'),
  url(r'^sales/data/$', SalesAjaxView.as_view(), name='sales-data'),
]
