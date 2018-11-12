from django.shortcuts import render
from .forms import ContactForm


def home_page(request):
  context = {
    "title": "Home page",
    "content": "Welcome to home page" 
  }
  if request.user.is_authenticated():
    context["logged_content"] = "logged users content"
  return render(request, "home_page.html", context)


def about_page(request):
  context = {
    "title": "About page",
    "content": "Welcome to about page"
  }
  return render(request, "home_page.html", context)


def contact_page(request):
  contact_form = ContactForm(request.POST or None)

  context = {
    "title": "Contact page",
    "content": "Welcome to contact page",
    "form": contact_form
  }
  if request.method == "POST":
    if contact_form.is_valid():
      print(contact_form.cleaned_data)
  return render(request, "contact/view.html", context)
