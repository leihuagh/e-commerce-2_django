from django.shortcuts import render

# Create your views here.

import stripe
stripe.api_key = 'sk_test_r3EsRHlzW559L1tojcPhYbBd'
STRIPE_PUB_KEY = 'pk_test_7iZ5TStSI7YoApUV7UruHTB3'

def payment_method_view(request):
  if request.method == 'POST':
    print(request.POST)
  context = {
    'publish_key': STRIPE_PUB_KEY
  }
  return render(request, 'billing/payment-method.html', context)