from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm

# Create your views here.

def checkout_address_create_view(request):
  form = AddressForm(request.POST or None)
  context = {
    "form": form
  }
  next_ = request.GET.get('next')
  next_post = request.POST.get('next')
  redirect_path = next_ or next_post or None
  if form.is_valid():
    print(request.POST)
    if is_safe_url(redirect_path, request.get_host()):
      return redirect(redirect_path)
    else:
      return redirect("cart:checkout")
  return redirect("cart:checkout")
