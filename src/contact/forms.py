from django import forms

from .models import Contact


class ContactUsForm(forms.ModelForm):
  fullname = forms.CharField(
    label='Full Name',
    widget=forms.TextInput(
      attrs={
        "class": "form-control",
        "placeholder": "Full Name",
      }
    )
  )
  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={
        "class": "form-control",
        "placeholder": "Email"
      }
    )
  )
  content = forms.CharField(
    widget=forms.Textarea(
      attrs={
        "class": "form-control",
        "placeholder": "Content"
      }
    )
  )

  class Meta:
    model = Contact
    fields = [
      'fullname',
      'email',
      'content'
    ]
  
  def clean_email(self):
    email = self.cleaned_data.get("email")
    if not "gmail.com" in email:
      raise forms.ValidationError("Email has to be gmail.com")
    return email
