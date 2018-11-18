from django.conf.urls import url

from .views import RegisterView, login_page, logout_page, guest_register_view

urlpatterns = [
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^login/$', login_page, name='login'),
  url(r'^logout/$', logout_page, name='logout'),
  url(r'^register/guest/$', guest_register_view, name='guest_register'),
]

