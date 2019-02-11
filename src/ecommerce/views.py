from django.shortcuts import render

from django.views.generic import TemplateView


class HomeView(TemplateView):
  template_name = "home_page.html"

  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    context['title'] = 'Home page'
    context['content'] = "Welcome to home page"
    if self.request.user.is_authenticated():
      context["logged_content"] = self.request.user
    return context


class AboutView(TemplateView):
  template_name = "home_page.html"

  def get_context_data(self, **kwargs):
    context = super(AboutView, self).get_context_data(**kwargs)
    context['title'] = 'About page'
    context['content'] = "Welcome to about page"
    return context
