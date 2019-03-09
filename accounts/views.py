from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, DetailView, UpdateView, View
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from ecommerce.mixins import (
  NextUrlMixin,
  RequestFormAttachMixin
)
from .forms import (
  LoginForm,
  RegisterForm,
  GuestForm,
  ReactivateEmailForm,
  UserDetailChangeForm
)
from .models import (
  GuestEmail,
  EmailActivation
)
from .signals import user_logged_in


class RegisterView(CreateView):
  form_class = RegisterForm
  template_name = 'accounts/register.html'
  success_url = reverse_lazy('accounts:login')


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
  form_class = LoginForm
  template_name = 'accounts/login.html'
  success_url = reverse_lazy('home')
  default_next = reverse_lazy('home')

  def form_valid(self, form):
    next_path = self.get_next_url()
    return redirect(next_path)


class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
  form_class = GuestForm
  default_next = reverse_lazy('accounts:register')

  def get_success_url(self):
    return self.get_next_url()

  def form_invalid(self, form):
    return redirect(self.default_next)


class AccountHomeView(LoginRequiredMixin, DetailView):
  template_name = 'accounts/home.html'

  def get_object(self):
    return self.request.user


class AccountEmailActivateView(FormMixin, View):
  success_url = reverse_lazy('accounts:login')
  form_class = ReactivateEmailForm
  key = None

  def get(self, request, key=None, *args, **kwargs):
    self.key = key
    if key is not None:
      qs = EmailActivation.objects.filter(key__iexact=key)
      confirm_qs = qs.confirmable()
      if confirm_qs.count() == 1:
        obj = confirm_qs.first()
        obj.activate()
        messages.success(request, "Your email has been confirmed. Please login.")
        return redirect("accounts:login")
      else:
        activated_qs = qs.filter(activated=True)
        if activated_qs.exists():
          reset_link = reverse("password_reset")
          msg = """Your email has already been confirmed
          Do you need to <a href="{link}">reset your password</a>?
          """.format(link=reset_link)
          messages.success(request, mark_safe(msg))
          return redirect("accounts:login")
    context = {'form': self.get_form(), 'key': self.key}
    return render(request, 'registration/activation-error.html', context)

  def post(self, request, *args, **kwargs):
    form = self.get_form()
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
    request = self.request
    msg = "Activation link sent, please check your email."
    messages.success(request, msg)
    email = form.cleaned_data.get("email")
    obj = EmailActivation.objects.email_exists(email).first()
    user = obj.user 
    new_activation = EmailActivation.objects.create(user=user, email=email)
    new_activation.send_activation()
    return super(AccountEmailActivateView, self).form_valid(form)

  def form_invalid(self, form):
    context = {'form': form, 'key': self.key}
    return render(self.request, 'registration/activation-error.html', context)


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
  form_class = UserDetailChangeForm
  template_name = 'accounts/detail-update-view.html'

  def get_object(self):
    return self.request.user

  def get_context_data(self, *args, **kwargs):
    context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Change Your Account Details'
    return context

  def get_success_url(self):
    return reverse("accounts:home")
