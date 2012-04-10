from django import forms
from apps.userprof.models import *
from django.contrib.auth.models import User

class change_password_form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Current password"}), label="")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"New password"}), label="")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"New password (re-type)"}), label="")

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            pwd1 = self.cleaned_data['password1']
            pwd2 = self.cleaned_data['password2']
            if pwd1 == pwd2:
                return pwd2
        raise forms.ValidationError("New password does not match :sosad:")


class edit_profile_form(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    website_blog = forms.CharField(label="Website/blog", required=False,
        widget=forms.TextInput(attrs={"placeholder": "http://"}))
    location = forms.CharField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea)


class register_form(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First name"}), label="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Last name"}), label="")
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}), label="")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Re-type password"}), label="")
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Email"}), label="")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError('Username is not available!')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError('Email is not available!')

    def clean_password2(self):
        if 'password' in self.cleaned_data:
            pwd = self.cleaned_data['password']
            pwd2 = self.cleaned_data['password2']
            if pwd == pwd2:
                return pwd2
        else:
            raise forms.ValidationError('Password does not match!')

