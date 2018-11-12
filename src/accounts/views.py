from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm
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
  
  if form.is_valid():
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect("/")
    else:
      print("Error while login")
  return render(request, "accounts/login.html", context)

def logout_page(request):
  logout(request)
  return redirect('accounts:login')