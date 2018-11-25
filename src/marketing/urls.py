from django.conf.urls import url

from .views import (
  marketing_home,
  MarketingPreferenceUpdateView
  )

urlpatterns = [
  url(r'^$', marketing_home, name='home'),
  url(r'^email/$', MarketingPreferenceUpdateView.as_view(), name='email'),
]

