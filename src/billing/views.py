from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from django.views.generic import View
import stripe

from .models import (
  BillingProfile,
  Card
)


STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY')
stripe.api_key = STRIPE_SECRET_KEY


class PaymentMethodView(View):
  template_name = 'billing/payment-method.html'

  def get(self, request):
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
    return render(request, self.template_name, context)


class PaymentMethodCreateView(View):

  def post(self, request):
    if request.method == 'POST' and request.is_ajax():
      billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
      if not billing_profile:
        return HttpResponse({"message": "can not find this user"}, status=401)
      token = request.POST.get('token')
      if token is not None:
        new_card_obj = Card.objects.add_new(billing_profile, token)
      return JsonResponse({"message": "Success! Your cart was added successfully!"})
    return HttpResponse("error", status=401)
