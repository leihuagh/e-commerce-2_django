from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation

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
  email = forms.EmailField(label='Email')
  password = forms.CharField(widget=forms.PasswordInput())

  def __init__(self, request, *args, **kwargs):
    self.request = request
    super(LoginForm, self).__init__(*args, **kwargs)

  def clean(self):
    request = self.request
    data = self.cleaned_data
    email  = data.get("email")
    password  = data.get("password")
    user = authenticate(request, username=email, password=password)
    if user is None:
      raise forms.ValidationError("Invalid credentials")
    login(request, user)
    self.user = user
    return data


class RegisterForm(forms.ModelForm):
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
    user = super(RegisterForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    user.is_active = False
    # obj = EmailActivation.objects.create(user=user)
    # obj.send_activation_email()
    if commit:
      user.save()
    return user


class GuestForm(forms.Form):
  email = forms.EmailField()


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