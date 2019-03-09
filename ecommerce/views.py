from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
  template_name = "about.html"

  def get_context_data(self, **kwargs):
    context = super(AboutView, self).get_context_data(**kwargs)
    context['title'] = 'About page'
    context['content'] = "Welcome to about page"
    return context
