from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from products.models import Product

# Create your views here.


class SearchProductView(ListView):
  template_name = "search/view.html"

  def get_context_data(self, *args, **kwargs):
    context = super(SearchProductView, self).get_context_data(*args, **kwargs)
    context['query'] = self.request.GET.get('q')
    return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    query = request.GET.get('q', None)
    print(query)
    if query is not None:
      lookups = Q(title__icontains=query) | Q(description__icontains=query)
      return Product.objects.filter(lookups).distinct()
    # return Product.objects.none()
    return Product.objects.featured()