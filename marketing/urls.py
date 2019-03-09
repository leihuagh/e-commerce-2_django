from django.conf.urls import url

from .views import (
  MarketingPreferenceUpdateView,
  MailchimpWebhookView
)


urlpatterns = [
  url(r'^email/$', MarketingPreferenceUpdateView.as_view(), name='email'),
  url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
]
