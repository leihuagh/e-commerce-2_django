from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Product

# Create your views here.

class ProductFeaturedListView(ListView):
  template_name = "products/list.html"

  def get_queryset(self, *args, **kwargs):
    request = self.request
    return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
  queryset = Product.objects.all().featured()
  template_name = "products/featured-detail.html"



class ProductListView(ListView):
  # queryset = Product.objects.all()
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    return Product.objects.all()
     


def product_list_view(request):
  queryset = Product.objects.all()
  context = {
    'object_list': queryset
  }
  return render(request, 'products/list.html', context)


class ProductDetailSlugView(DetailView):
  queryset = Product.objects.all()
  template_name = "products/detail.html"

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



class ProductDetailView(DetailView):
  # queryset = Product.objects.all()
  template_name = "products/detail.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    context['abc'] = "some other content"
    return context

  def get_object(self, *args, **kwargs):
    request = self.request
    pk = self.kwargs.get('pk')
    instance = Product.objects.get_by_id(pk)
    if instance is None:
      raise Http404("Product does't exist")
    return instance

  # def get_queryset(self, *args, **kwargs):
  #   request = self.request
  #   pk = self.kwargs.get('pk')
  #   return Product.objects.filter(pk=pk)


def product_detail_view(request, pk, *args, **kwargs):
  # instance = Product.objects.get(pk=pk)
  # instance = get_object_or_404(Product, pk=pk)
  # try:
  #   instance = Product.objects.get(id=pk)
  # except Product.DoesNotExist:
  #   print('No product found with this id : ', pk)
  #   raise Http404("Product does't exist")
  # except:
  #   print('Unknown error')
  
  instance = Product.objects.get_by_id(pk)
  if instance is None:
    raise Http404("Product does't exist")



  # qs = Product.objects.filter(id=pk)
  # if qs.exists() and qs.count() == 1:
  #   instance = qs.first()
  # else:
  #   raise Http404("Product does't exist")

  context = {
    'object': instance,
    'abc': "some other content from function based view"
  }
  return render(request, 'products/detail.html', context)

