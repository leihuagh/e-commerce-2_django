from django.conf.urls import url

from .views import (
  ProductListView, 
  # ProductDetailView, 
  ProductDetailSlugView, 
  # product_list_view, 
  # product_detail_view, 
  # ProductFeaturedListView, 
  # ProductFeaturedDetailView
  )

urlpatterns = [
  url(r'^$', ProductListView.as_view()),
  # url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view()),
  url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
  # url(r'^featured/$', ProductFeaturedListView.as_view()),
  # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),



  # url(r'^fbv/$', product_list_view),
  # url(r'^(?P<pk>\d+)/fbv/$', product_detail_view),
]

