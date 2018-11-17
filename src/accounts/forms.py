from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
  username = forms.CharField()
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())
  password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

  def clean_username(self):
    username = self.cleaned_data.get("username")
    qs = User.objects.filter(username=username)
    if qs.exists():
      raise forms.ValidationError("Username is already taken!")
    return username
  
  def clean_email(self):
    email = self.cleaned_data.get("email")
    qs = User.objects.filter(email=email)
    if qs.exists():
      raise forms.ValidationError("email is already taken!")
    return email

  def clean(self):
    data = self.cleaned_data
    password = data.get("password")
    password2 = data.get("password2")
    if password2 != password:
      raise forms.ValidationError("Password must match!")
    return data


class GuestForm(forms.Form):
  email = forms.EmailField()


class UserAdminCreationForm(forms.ModelForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('email',)

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
    fields = ('email', 'password', 'active', 'admin')

  def clean_password(self):
    return self.initial["password"]