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
        fields = ['title', 'content']

class ImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['avatar']


STATUS_CHOICES = [
    ('0%', '0%'),
    ('10%', '10%'),
    ('20%', '20%'),
    ('30%', '30%'),
    ('40%', '40%'),
    ('50%', '50%'),
    ('60%', '60%'),
    ('70%', '70%'),
    ('80%', '80%'),
    ('90%', '90%'),
    ('100%', '100%'),

]

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class TaskForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    status = forms.CharField(widget=forms.Select(choices=STATUS_CHOICES))
    user = UserModelChoiceField( queryset=User.objects.all() )
#widget=forms.Select(choices=USERS_CHOICES)
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'user']
