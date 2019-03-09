from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import Http404, HttpResponse
from wsgiref.util import FileWrapper
from mimetypes import guess_type
import os

from ecommerce.utils import render_to_pdf
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from orders.models import ProductPurchase
from .models import (
  Product,
  ProductFile
)


class HomePageListView(ListView):
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    context = super(HomePageListView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_queryset(self, *args, **kwargs):
    return Product.objects.all().order_by('-id')


class ProductListView(ListView):
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_queryset(self, *args, **kwargs):
    return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
  queryset = Product.objects.all()
  template_name = "products/detail.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_object(self, *args, **kwargs):
    request = self.request
    slug = self.kwargs.get('slug')
    try:
      instance = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
      raise Http404("Product does't exist")
    except Product.MultipleObjectsReturned:
      qs = Product.objects.filter(slug=slug, active=True)
      instance = qs.first()
    except:
      raise Http404('Unknown error') 
    return instance


class UserProductHistoryView(LoginRequiredMixin, ListView):
  template_name = "products/user-history.html"
  def get_context_data(self, *args, **kwargs):
    context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
    return views


class ProductDownloadView(View):
  def get(self, request, *args, **kwargs):
    slug = kwargs.get('slug')
    pk = kwargs.get('pk')
    downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
    if downloads_qs.count() != 1:
      raise Http404("Download not found")
    download_obj = downloads_qs.first()

    can_download = False
    user_ready = True
    if download_obj.user_required:
      if not request.user.is_authenticated():
        user_ready = False
    purchased_products = Product.objects.none()
    if download_obj.free:
      can_download = True
      user_ready = True
    else:
      purchased_products = ProductPurchase.objects.products_by_request(request)
      if download_obj.product in purchased_products:
        can_download = True
    if not can_download or not user_ready:
      messages.error(request, "You do not have access to download this item")
      return redirect(download_obj.get_default_url())

    file_root = settings.PROTECTED_ROOT
    filepath = download_obj.file.path
    final_filepath = os.path.join(file_root, filepath)
    with open(final_filepath, 'rb') as f:
      wrapper = FileWrapper(f)
      mimetype = 'application/force-download'
      gussed_mimetype = guess_type(filepath)[0]
      if gussed_mimetype:
        mimetype = gussed_mimetype
      response = HttpResponse(wrapper, content_type=mimetype)
      response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
      response["X-SendFile"] = str(download_obj.name)
      return response


class ProductDetailGeneratePDFView(View):
  def get(self, request, *args, **kwargs):
    qs = Product.objects.filter(slug=self.kwargs.get('slug'))
    if qs.count() == 1:
      product = qs.first()
      context = {
        'product_id': product.id,
        'title': product.title,
        'slug': product.slug,
        'timestamp': product.timestamp,
        'price': product.price,
        'description': product.description,
        'url': product.get_absolute_url,
        'full_url': settings.BASE_URL + product.image.url,
      }
      if product.image:
        context['image'] = product.image.url
      pdf = render_to_pdf('pdf/product-detail.html', context)
      if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Product-{}-{}-detail.pdf".format(product.id, product.slug)
        content = "inline; filename={}".format(filename)
        download = request.GET.get("download")
        if download:
          content = "attachment; filename={}".format(filename)
        response['Content-Disposition'] = content
        return response
      return HttpResponse("Not found")
    return redirect("products:list")
