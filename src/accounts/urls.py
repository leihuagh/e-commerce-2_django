from django.conf.urls import url

from .views import register_page, login_page, logout_page

urlpatterns = [
  url(r'^register/$', register_page, name='register'),
  url(r'^login/$', login_page, name='login'),
  url(r'^logout/$', logout_page, name='logout'),
]

