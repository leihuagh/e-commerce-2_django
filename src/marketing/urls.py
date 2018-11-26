from django.conf.urls import url

from .views import (
  marketing_home,
  MarketingPreferenceUpdateView,
  MailchimpWebhookView
  )

urlpatterns = [
  url(r'^$', marketing_home, name='home'),
  url(r'^email/$', MarketingPreferenceUpdateView.as_view(), name='email'),
  url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
]

