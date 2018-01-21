from django.contrib.auth.models import User
from django import forms
from .models import *


class IssueForm(forms.Form):

    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=500)
    milestone = forms.CharField(max_length=100)


class LabelForm(forms.Form):

    name = forms.CharField(max_length=100)
    color = forms.CharField(max_length=7)


class LocalRepositoryForm(forms.Form):

    repo_name = forms.CharField(max_length=70)


class GitRepositoryForm(forms.Form):

    repo_url = forms.CharField(max_length=150)


class MilestoneForm(forms.Form):

    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500)


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


class WikiForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = WikiPage
        fields = '__all__'
