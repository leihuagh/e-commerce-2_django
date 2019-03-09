from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.generic.edit import FormMixin

from .forms import ContactUsForm
from .models import Contact


class ContactUsView(View):
  form_class = ContactUsForm
  template_name = 'contact/home.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class()
    if request.user.is_authenticated():
      form = self.form_class(initial={'fullname': request.user.full_name, 'email': request.user.email})
    context = {'form': form, 'content': "Welcome to contact us page"}
    return render(request, self.template_name, context)

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)
  
  def form_valid(self, form):
    form.save()
    return JsonResponse({"message": "Thank you for your submission"})

  def form_invalid(self, form):
    if form.errors:
      errors = form.errors.as_json()
      if self.request.is_ajax():
        return HttpResponse(errors, status=400, content_type='application/json')
