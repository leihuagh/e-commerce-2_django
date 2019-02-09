from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .forms import ContactForm
from .models import Contact

# Create your views here.


def contact_page(request):
  contact_form = ContactForm(request.POST or None)

  context = {
    "title": "Contact page",
    "content": "Welcome to contact page",
    "form": contact_form
  }
  if request.method == "POST":
    if contact_form.is_valid():
      if request.is_ajax():
        data = contact_form.cleaned_data
        fullname = data.get('fullname')
        email = data.get('email')
        content = data.get('content')
        Contact.objects.create(fullname=fullname, email=email, content=content)
        return JsonResponse({"message": "Thank you for your submission"})
    
    if contact_form.errors:
      errors = contact_form.errors.as_json()
      if request.is_ajax():
        return HttpResponse(errors, status=400, content_type='application/json')
  return render(request, "contact/home.html", context)