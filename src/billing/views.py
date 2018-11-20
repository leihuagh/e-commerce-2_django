from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url

# Create your views here.

import stripe
stripe.api_key = 'sk_test_r3EsRHlzW559L1tojcPhYbBd'
STRIPE_PUB_KEY = 'pk_test_7iZ5TStSI7YoApUV7UruHTB3'

def payment_method_view(request):
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
    print(request.POST)
    return JsonResponse({"message": "Success! Your cart was added successfully!"})
  return HttpResponse("error", status_code=401)


def billing_home(request):
  return 'billing'