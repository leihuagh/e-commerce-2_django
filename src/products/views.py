from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Product, ProductFile
from carts.models import Cart
from orders.models import ProductPurchase
from analytics.mixins import ObjectViewedMixin

from ecommerce.utils import render_to_pdf

import os
from wsgiref.util import FileWrapper
from mimetypes import guess_type

from django.conf import settings


# Create your views here.

# class ProductFeaturedListView(ListView):
#   template_name = "products/list.html"

#   def get_queryset(self, *args, **kwargs):
#     request = self.request
#     return Product.objects.all().featured()


# class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
#   queryset = Product.objects.all().featured()
#   template_name = "products/featured-detail.html"



class ProductListView(ListView):
  # queryset = Product.objects.all()
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    return Product.objects.all()
     


# def product_list_view(request):
#   queryset = Product.objects.all()
#   context = {
#     'object_list': queryset
#   }
#   return render(request, 'products/list.html', context)


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
    # instance = get_object_or_404(Product, slug=slug, active=True)
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
    # return redirect(download_obj.get_default_url())



class ProductDetailGeneratePDFView(View):
  def get(self, request, *args, **kwargs):
    qs = Product.objects.filter(slug=self.kwargs.get('slug'))
    if qs.count() == 1:
      product = qs.first()
      # request.META['HTTP_HOST']
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
      # return HttpResponse(pdf, content_type='application/pdf')
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

# class ProductDetailView(ObjectViewedMixin, DetailView):
#   # queryset = Product.objects.all()
#   template_name = "products/detail.html"

#   def get_context_data(self, *args, **kwargs):
#     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#     context['abc'] = "some other content"
#     return context

#   def get_object(self, *args, **kwargs):
#     request = self.request
#     pk = self.kwargs.get('pk')
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#       raise Http404("Product does't exist")
#     return instance

#   # def get_queryset(self, *args, **kwargs):
#   #   request = self.request
#   #   pk = self.kwargs.get('pk')
#   #   return Product.objects.filter(pk=pk)


# def product_detail_view(request, pk, *args, **kwargs):
#   # instance = Product.objects.get(pk=pk)
#   # instance = get_object_or_404(Product, pk=pk)
#   # try:
#   #   instance = Product.objects.get(id=pk)
#   # except Product.DoesNotExist:
#   #   print('No product found with this id : ', pk)
#   #   raise Http404("Product does't exist")
#   # except:
#   #   print('Unknown error')
  
#   instance = Product.objects.get_by_id(pk)
#   if instance is None:
#     raise Http404("Product does't exist")

#   # qs = Product.objects.filter(id=pk)
#   # if qs.exists() and qs.count() == 1:
#   #   instance = qs.first()
#   # else:
#   #   raise Http404("Product does't exist")

#   context = {
#     'object': instance,
#     'abc': "some other content from function based view"
#   }
#   return render(request, 'products/detail.html', context)

