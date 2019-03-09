from django.http import JsonResponse

from carts.models import Cart


def cart_home(request):
  cart_obj, new_obj = Cart.objects.new_or_get(request)
  products = [{"id": x.id, "name": x.name, "price": x.price, "url": x.get_absolute_url()} for x in cart_obj.products.all().order_by('-id')]
  cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
  return JsonResponse(cart_data)
