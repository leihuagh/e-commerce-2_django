from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, View
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse_lazy

from billing.models import BillingProfile
from .forms import (
  AddressCheckoutForm,
  AddressForm
)
from .models import Address


class AddressListView(LoginRequiredMixin, ListView):
  template_name = 'addresses/list.html'

  def get_queryset(self):
    request = self.request
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    return Address.objects.filter(billing_profile=billing_profile)


class AddressCreateView(LoginRequiredMixin, CreateView):
  template_name = 'addresses/update.html'
  form_class = AddressForm
  success_url = reverse_lazy('addresses:list')

  def form_valid(self, form):
    request = self.request
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    instance = form.save(commit=False)
    instance.billing_profile = billing_profile
    instance.save()
    return super(AddressCreateView, self).form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'addresses/update.html'
  form_class = AddressForm
  success_url = reverse_lazy('addresses:list')

  def get_queryset(self):
    request = self.request
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    return Address.objects.filter(billing_profile=billing_profile)


class CheckoutAddressCreateView(View):

  def post(self, request):
    form = AddressCheckoutForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
      instance = form.save(commit=False)
      billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
      if billing_profile is not None:
        address_type = request.POST.get('address_type', 'shipping')
        instance.billing_profile = billing_profile
        instance.address_type = address_type
        instance.save()
        request.session[address_type + '_address_id'] = instance.id
      else:
        return redirect("cart:checkout")
      if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
    return redirect("cart:checkout")


class CheckoutAddressReuseView(View):

  def post(self, request):
    if request.user.is_authenticated():
      next_ = request.GET.get('next')
      next_post = request.POST.get('next')
      redirect_path = next_ or next_post or None
      if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', None)
        address_type = request.POST.get('address_type', 'shipping')
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if shipping_address is not None:
          qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
          if qs.exists():
            request.session[address_type + '_address_id'] = shipping_address
          if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("cart:checkout")
