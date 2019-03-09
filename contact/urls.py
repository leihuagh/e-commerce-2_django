from django.conf.urls import url

from .views import (
  ContactUsView,
)


urlpatterns = [
  url(r'^$', ContactUsView.as_view(), name='home'),
]
