from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from products.views import HomePageListView
from .views import AboutView


urlpatterns = [
  url(r'^$', HomePageListView.as_view(), name='home'),
  url(r'^about/$', AboutView.as_view(), name='about'),
  url(r'^settings/$', RedirectView.as_view(url='/account')),
  url(r'^accounts/$', RedirectView.as_view(url='/account')),
  url(r'^account/', include('accounts.urls', namespace='accounts')),
  url(r'^accounts/', include('accounts.passwords.urls')),
  url(r'^products/', include('products.urls', namespace='products')),
  url(r'^search/', include('search.urls', namespace='search')),
  url(r'^cart/', include('carts.urls', namespace='cart')),
  url(r'^orders/', include('orders.urls', namespace='orders')),
  url(r'^billing/', include('billing.urls', namespace='billing')),
  url(r'^address/$', RedirectView.as_view(url='/addresses')),
  url(r'^addresses/', include('addresses.urls', namespace='addresses')),
  url(r'^analytics/', include('analytics.urls', namespace='analytics')),
  url(r'^marketing/', include('marketing.urls', namespace='marketing')),
  url(r'^contact/', include('contact.urls', namespace='contact')),
  url(r'^admin/', admin.site.urls),
  
  url(r'^cart-api/', include('carts.api.urls', namespace='cart-api')),
]

if settings.DEBUG:
  urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
