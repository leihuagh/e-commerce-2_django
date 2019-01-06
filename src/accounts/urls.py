from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import RegisterView, LoginView, guest_register_view, AccountHomeView

urlpatterns = [
  url(r'^$', AccountHomeView.as_view(), name='home'),
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^login/$', LoginView.as_view(), name='login'),
  url(r'^logout/$', LogoutView.as_view(), name='logout'),
  url(r'^register/guest/$', guest_register_view, name='guest_register'),
]

