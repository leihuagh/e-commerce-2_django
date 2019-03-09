from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect

from ecommerce.utils import render_to_pdf
from billing.models import BillingProfile
from .models import (
  Order,
  ProductPurchase
)


class OrderListView(LoginRequiredMixin, ListView):

  def get_queryset(self):
    return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):

  def get_object(self):
    qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
    if qs.count() == 1:
      return qs.first()
    raise Http404


class LibraryView(LoginRequiredMixin, ListView):
  template_name = 'orders/library.html'
  
  def get_queryset(self):
    return ProductPurchase.objects.products_by_request(self.request)


class VerifyOwnership(View):
  def get(self, request, *args, **kwargs):
    if request.is_ajax():
      product_id = request.GET.get('product_id', None)
      if product_id is not None:
        product_id = int(product_id)
        ownership_ids = ProductPurchase.objects.products_by_id(request)
        if product_id in ownership_ids:
          return JsonResponse({'owner': True})
      return JsonResponse({'owner': False})
    raise Http404


class OrderDetailGeneratePDFView(View):
  def get(self, request, *args, **kwargs):
    qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
    if qs.count() == 1:
      order = qs.first()
      context = {
        'user': request.user,
        'order_id': order.order_id,
        'cart_items': order.cart,
        'shipping_address_final': order.shipping_address_final,
        'billing_address_final': order.billing_address_final,
        'cart': order.cart,
        'shipping_total': order.shipping_total,
        'subtotal_percentage': settings.SUB_TOTAL_PERCENTAGE,
        'fee': round(order.cart.total - order.cart.subtotal, 2),
        'total': order.total,
        'status': order.get_status,
      }
      pdf = render_to_pdf('pdf/order-detail.html', context)
      if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Order-{}-detail.pdf".format(order.order_id)
        content = "inline; filename={}".format(filename)
        download = request.GET.get("download")
        if download:
          content = "attachment; filename={}".format(filename)
        response['Content-Disposition'] = content
        return response
      return HttpResponse("Not found")
    return redirect("orders:list")
