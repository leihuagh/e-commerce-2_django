from django.shortcuts import render

from django.views.generic import TemplateView


def home_page(request):
  context = {
    "title": "Home page",
    "content": "Welcome to home page" 
  }
  if request.user.is_authenticated():
    context["logged_content"] = request.user
  return render(request, "home_page.html", context)


class AboutView(TemplateView):
  template_name = "home_page.html"

  def get_context_data(self, **kwargs):
    context = super(AboutView, self).get_context_data(**kwargs)
    context['title'] = 'About page'
    context['content'] = "Welcome to about page"
    return context
