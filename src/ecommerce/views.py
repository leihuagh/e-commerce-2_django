from django.shortcuts import render


def home_page(request):
  context = {
    "title": "Home page",
    "content": "Welcome to home page" 
  }
  if request.user.is_authenticated():
    context["logged_content"] = request.user
  return render(request, "home_page.html", context)


def about_page(request):
  context = {
    "title": "About page",
    "content": "Welcome to about page"
  }
  return render(request, "home_page.html", context)
