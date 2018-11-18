from django.conf.urls import url

from .views import (
  analytics_home,
)

urlpatterns = [
  url(r'^$', analytics_home, name='home'),

]

