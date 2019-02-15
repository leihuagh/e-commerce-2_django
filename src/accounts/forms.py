from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import (
  EmailActivation,
  GuestEmail
)

User = get_user_model()


class ReactivateEmailForm(forms.Form):
  email = forms.EmailField()

  def clean_email(self):
    email = self.cleaned_data.get('email')
    qs = EmailActivation.objects.email_exists(email) 
    if not qs.exists():
      register_link = reverse("accounts:register")
      msg = """This email does not exists, would you like to <a href="{link}">register</a>?
      """.format(link=register_link)
      raise forms.ValidationError(mark_safe(msg))
    return email


class LoginForm(forms.Form):
  email = forms.EmailField(
    label='Email',
    widget=forms.EmailInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Email"
      }
    )
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "password"
      }
    )
  )

  def __init__(self, request, *args, **kwargs):
    self.request = request
    super(LoginForm, self).__init__(*args, **kwargs)

  def clean(self):
    request = self.request
    data = self.cleaned_data
    email  = data.get("email")
    password  = data.get("password")
    qs = User.objects.filter(email=email)
    if qs.exists():
      not_active = qs.filter(is_active=False)
      if not_active.exists():
        link = reverse("accounts:resend-activation")
        reconfirm_msg = """Go to <a href='{resend_link}'>
        resend confirmation email</a>.""".format(resend_link=link)
        confirm_email = EmailActivation.objects.filter(email=email)
        is_confirmable = confirm_email.confirmable().exists()
        if is_confirmable:
          msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
          raise forms.ValidationError(mark_safe(msg1))
        email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
        if email_confirm_exists:
          msg2 = "Email not confirmed. " + reconfirm_msg
          raise forms.ValidationError(mark_safe(msg2))
        if not is_confirmable and not email_confirm_exists:
          raise forms.ValidationError("This user is inactive.")
    user = authenticate(request, username=email, password=password)
    if user is None:
      raise forms.ValidationError("Invalid credentials")
    login(request, user)
    self.user = user
    return data


class RegisterForm(forms.ModelForm):
  email = forms.EmailField(
    label='Email',
    widget=forms.EmailInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Email"
      }
    )
  )
  full_name = forms.CharField(
    label='Full Name',
    widget=forms.TextInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Full Name"
      }
    )
  )
  password1 = forms.CharField(
    label='Password',
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "password"
      }
    )
  )
  password2 = forms.CharField(
    label='Password confirmation',
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Password confirmation"
      }
    )
  )

  class Meta:
    model = User
    fields = ('email', 'full_name', )

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords don't match")
    return password2

  def save(self, commit=True):
    user = super(RegisterForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    user.is_active = False
    if commit:
      user.save()
    return user


class GuestForm(forms.ModelForm):

  class Meta:
    model = GuestEmail
    fields = [
      'email'
    ]

  def __init__(self, request, *args, **kwargs):
    self.request = request
    super(GuestForm, self).__init__(*args, **kwargs)

  def save(self, commit=True):
    obj = super(GuestForm, self).save(commit=False)
    if commit:
      obj.save()
      request = self.request
      request.session['guest_email_id'] = obj.id
    return obj


class UserDetailChangeForm(forms.ModelForm):
  full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

  class Meta:
    model = User
    fields = ['full_name']


class UserAdminCreationForm(forms.ModelForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('email', 'full_name', )

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords don't match")
    return password2

  def save(self, commit=True):
    user = super(UserAdminCreationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user


class UserAdminChangeForm(forms.ModelForm):
  password = ReadOnlyPasswordHashField()

  class Meta:
    model = User
    fields = ('email', 'full_name', 'password', 'is_active', 'admin')

  def clean_password(self):
    return self.initial["password"]
