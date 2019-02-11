from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .forms import ContactUsForm
from .models import Contact
from django.views.generic.edit import FormMixin
from django.views.generic import View

# Create your views here.


# class ContactUsView(FormMixin, View):
class ContactUsView(View):
  form_class = ContactUsForm
  template_name = 'contact/home.html'

  def get(self, request, *args, **kwargs):
    # context = {'form': self.get_form(), 'content': "Welcome to contact us page"}
    context = {'form': self.form_class(), 'content': "Welcome to contact us page"}
    return render(request, self.template_name, context)

  def post(self, request, *args, **kwargs):
    # form = self.get_form()
    form = self.form_class(request.POST)
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)
  
  def form_valid(self, form):
    data = form.cleaned_data
    fullname = data.get('fullname')
    email = data.get('email')
    content = data.get('content')
    Contact.objects.create(fullname=fullname, email=email, content=content)
    return JsonResponse({"message": "Thank you for your submission"})

  def form_invalid(self, form):
    if form.errors:
      errors = form.errors.as_json()
      if self.request.is_ajax():
        return HttpResponse(errors, status=400, content_type='application/json')
