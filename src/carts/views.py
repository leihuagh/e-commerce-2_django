from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
import stripe

from accounts.models import GuestEmail
from accounts.forms import (
  LoginForm,
  GuestForm
)
from addresses.forms import AddressCheckoutForm
from addresses.models import Address
from billing.models import BillingProfile
from products.models import Product
from orders.models import Order
from .models import Cart


STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY')
stripe.api_key = STRIPE_SECRET_KEY


class CartHomeView(ListView):
  template_name = 'carts/home.html'
  queryset = ''

  def get_context_data(self, **kwargs):
    context = super(CartHomeView, self).get_context_data(**kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context


class CartUpdateView(View):

  def post(self, request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
      try:
        product_obj = Product.objects.get(id=product_id)
      except Product.DoesNotExist:
        return redirect('cart:home')  
      cart_obj, new_obj = Cart.objects.new_or_get(request)
      if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        added = False
      else:
        cart_obj.products.add(product_obj)
        added = True
      request.session['cart_items'] = cart_obj.products.count()
      if request.is_ajax():
        json_data = {
          "added": added,
          "removed": not added,
          "cartItemCount": cart_obj.products.count()
        }
        return JsonResponse(json_data, status=200)
    return redirect('cart:home')


class CheckoutHomeView(View):
  template_name = 'carts/checkout.html'

  def get(self, request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
      return redirect('cart:home')
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    shipping_address_required = not cart_obj.is_digital
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_address_id = request.session.get('billing_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    
    address_qs = None
    has_card = False
    if billing_profile is not None:
      if request.user.is_authenticated():
        address_qs = Address.objects.filter(billing_profile=billing_profile)
      order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
      if shipping_address_id:
        order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        del request.session['shipping_address_id']
      if billing_address_id:
        order_obj.billing_address = Address.objects.get(id=billing_address_id)
        del request.session['billing_address_id']
      if shipping_address_id or billing_address_id:
        order_obj.save()
      has_card = billing_profile.has_card
    context = {
      'object': order_obj,
      'billing_profile': billing_profile,
      'login_form': login_form,
      'guest_form': guest_form,
      'address_form': address_form,
      'address_qs': address_qs,
      'has_card': has_card,
      'publish_key': STRIPE_PUB_KEY,
      'shipping_address_required': shipping_address_required,
    }
    return render(request, self.template_name, context)

  def post(self, request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    is_prepared = order_obj.check_done()
    if is_prepared:
      did_charge, crg_msg = billing_profile.charge(order_obj)
      if did_charge:
        order_obj.mark_paid()
        del request.session['cart_id']
        request.session['cart_items'] = 0
        if not billing_profile.user:
          billing_profile.set_cards_inactive()
        return redirect('cart:success')
      else:
        print(crg_msg)
        return redirect('cart:checkout')
    return redirect('cart:home')


class CheckoutDoneView(TemplateView):
  template_name = 'carts/checkout-done.html'
