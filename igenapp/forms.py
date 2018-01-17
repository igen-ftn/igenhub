from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User


class IssueForm(forms.Form):

    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=500)
    milestone = forms.CharField(max_length=100)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(render_value = True))
    email = forms.CharField(widget = forms.EmailInput)
    username = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class UserEditForm(forms.ModelForm):
    email = forms.CharField(widget = forms.EmailInput)
    username = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']