from django import forms

from igenapp.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    email = forms.CharField(widget = forms.EmailInput)
    class Meta:
        model = User
        fields = '__all__'