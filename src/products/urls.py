from django.conf.urls import url

from .views import ProductListView, ProductDetailView, product_list_view, product_detail_view

urlpatterns = [
  url(r'^$', ProductListView.as_view()),
  url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view()),



  url(r'^fbv/$', product_list_view),
  url(r'^(?P<pk>\d+)/fbv/$', product_detail_view),
]

