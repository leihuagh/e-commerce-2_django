from django.conf.urls import url

from .views import RegisterView, LoginView, logout_page, guest_register_view

urlpatterns = [
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^login/$', LoginView.as_view(), name='login'),
  url(r'^logout/$', logout_page, name='logout'),
  url(r'^register/guest/$', guest_register_view, name='guest_register'),
]

