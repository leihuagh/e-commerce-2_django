from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm

# Create your views here.

# def cart_create(user=None):
#   cart_obj = Cart.objects.create(user=None)
#   print('Create new cart')
#   return cart_obj



def cart_home(request):
  # if cart_id is None:
  #   cart_obj = cart_create()
  #   request.session['cart_id'] = cart_obj.id
  # else:


  # cart_id = request.session.get('cart_id', None)
  # qs = Cart.objects.filter(id=cart_id)
  # if qs.count() == 1:
  #   cart_obj = qs.first()
  #   if request.user.is_authenticated() and cart_obj.user is None:
  #     cart_obj.user = request.user
  #     cart_obj.save()
  # else:
  #   cart_obj = Cart.objects.new(user=request.user)
  #   request.session['cart_id'] = cart_obj.id

  cart_obj, new_obj = Cart.objects.new_or_get(request)
  # products = cart_obj.products.all()
  # total = 0
  # for x in products:
  #   total += x.price
  # cart_obj.total = total
  # cart_obj.save()
  context = {
    'cart' : cart_obj
  }
  return render(request, 'carts/home.html', context)


def cart_update(request):
  product_id = request.POST.get('product_id')
  if product_id is not None:
    try:
      product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
      return redirect('cart:home')  
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
      cart_obj.products.remove(product_obj) # cart_obj.products.remove(product_id)
    else:
      cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
    request.session['cart_items'] = cart_obj.products.count()
  # return  redirect(product_obj.get_absolute_url())
  return redirect('cart:home')

def checkout_home(request):
  cart_obj, cart_created = Cart.objects.new_or_get(request)
  order_obj = None
  if cart_created or cart_obj.products.count() == 0:
    return redirect('cart:home')
  else:
    order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
  user = request.user
  billing_profile = None
  login_form = LoginForm()

  if user.is_authenticated():
    billing_profile = None
  context = {
    'object': order_obj,
    'billing_profile': billing_profile,
    'login_form': login_form
  }
  return render(request, 'carts/checkout.html', context)