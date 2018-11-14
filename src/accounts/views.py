from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

# Create your views here.

User = get_user_model()


def register_page(request):
  form = RegisterForm(request.POST or None)
  context = {
    "form": form
  }
  if form.is_valid():
    username = form.cleaned_data.get("username")
    email = form.cleaned_data.get("email")
    password = form.cleaned_data.get("password")
    new_user = User.objects.create_user(username, email, password)
  return render(request, "accounts/register.html", context)

def login_page(request):
  form = LoginForm(request.POST or None)
  context = {
    "form": form
  }
  next_ = request.GET.get('next')
  next_post = request.POST.get('next')
  redirect_path = next_ or next_post or None
  if form.is_valid():
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      try:
        del request.session['guest_email_id']
      except:
        pass
      if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
      else:
        return redirect("home")
    else:
      print("Error while login")
  return render(request, "accounts/login.html", context)

def logout_page(request):
  logout(request)
  return redirect('accounts:login')


def guest_register_view(request):
  form = GuestForm(request.POST or None)
  context = {
    "form": form
  }
  next_ = request.GET.get('next')
  next_post = request.POST.get('next')
  redirect_path = next_ or next_post or None
  if form.is_valid():
    email = form.cleaned_data.get("email")
    new_guest_email = GuestEmail.objects.create(email=email)
    request.session['guest_email_id'] = new_guest_email.id
    if is_safe_url(redirect_path, request.get_host()):
      return redirect(redirect_path)
    else:
      return redirect("accounts:register")
  return redirect("accounts:register")