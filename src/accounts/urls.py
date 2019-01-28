from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import RegisterView, LoginView, guest_register_view, AccountHomeView, AccountEmailActivateView

urlpatterns = [
  url(r'^$', AccountHomeView.as_view(), name='home'),
  url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^login/$', LoginView.as_view(), name='login'),
  url(r'^logout/$', LogoutView.as_view(), name='logout'),
  url(r'^register/guest/$', guest_register_view, name='guest_register'),
]

