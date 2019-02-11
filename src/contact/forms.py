from django import forms


class ContactUsForm(forms.Form):
  fullname = forms.CharField(
    widget=forms.TextInput(
    attrs={
    "class": "form-control",
    "placeholder": "Name",
    "id": "form_full_name"
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

  def clean_email(self):
    email = self.cleaned_data.get("email")
    if not "gmail.com" in email:
      raise forms.ValidationError("Email has to be gmail.com")
    return email
