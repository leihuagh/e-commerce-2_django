from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product

# Create your views here.

class ProductListView(ListView):
  queryset = Product.objects.all()
  template_name = "products/list.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    return context


def product_list_view(request):
  queryset = Product.objects.all()
  context = {
    'object_list': queryset
  }
  return render(request, 'products/list.html', context)


class ProductDetailView(DetailView):
  queryset = Product.objects.all()
  template_name = "products/detail.html"

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    print(context)
    context['abc'] = "some other content"
    print(context)
    return context


def product_detail_view(request, pk, *args, **kwargs):
  # instance = Product.objects.get(pk=pk)
  instance = get_object_or_404(Product, pk=pk)
  context = {
    'object': instance,
    'abc': "some other content from function based view"
  }
  return render(request, 'products/detail.html', context)
