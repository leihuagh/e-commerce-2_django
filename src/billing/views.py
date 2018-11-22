from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .models import BillingProfile, Card

# Create your views here.

import stripe
# stripe.api_key = 'sk_test_r3EsRHlzW559L1tojcPhYbBd'
# STRIPE_PUB_KEY = 'pk_test_7iZ5TStSI7YoApUV7UruHTB3'
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_r3EsRHlzW559L1tojcPhYbBd')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', 'pk_test_7iZ5TStSI7YoApUV7UruHTB3')
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
  # if request.user.is_authenticated():
  #   billing_profile = request.user.billingprofile
  #   my_customer_id = billing_profile.customer_id
    
  billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
  if not billing_profile:
    return redirect('cart:home')

  next_url = None
  next_ = request.GET.get('next')
  if is_safe_url(next_, request.get_host()):
    next_url = next_
  context = {
    'publish_key': STRIPE_PUB_KEY,
    "next_url": next_url
  }
  return render(request, 'billing/payment-method.html', context)


def payment_method_create_view(request):
  if request.method == 'POST' and request.is_ajax():
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
      return HttpResponse({"message": "can not find this user"}, status_code=401)
    
    token = request.POST.get('token')
    if token is not None:
      # customer = stripe.Customer.retrieve(billing_profile.customer_id)
      # card_response = customer.sources.create(source=token)
      # new_card_obj = Card.objects.add_new(billing_profile, card_response)
      new_card_obj = Card.objects.add_new(billing_profile, token)
    return JsonResponse({"message": "Success! Your cart was added successfully!"})
  return HttpResponse("error", status_code=401)


def billing_home(request):
  return 'billing'