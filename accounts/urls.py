from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import RegisterView, LoginView, GuestRegisterView, AccountHomeView, AccountEmailActivateView, UserDetailUpdateView
from products.views import UserProductHistoryView

urlpatterns = [
  url(r'^$', AccountHomeView.as_view(), name='home'),
  url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
  url(r'^history/products/$', UserProductHistoryView.as_view(), name='user-product-history'),
  url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
  url(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^login/$', LoginView.as_view(), name='login'),
  url(r'^logout/$', LogoutView.as_view(), name='logout'),
  url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
]

