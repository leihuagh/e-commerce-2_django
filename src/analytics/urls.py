from django.conf.urls import url

from .views import (
  SalesView,
)

urlpatterns = [
  url(r'^sales/$', SalesView.as_view(), name='sales'),

]

