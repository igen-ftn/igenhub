from django import forms

from igenapp.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(render_value = True))
    email = forms.CharField(widget = forms.EmailInput)
    username = forms.CharField()
    class Meta:
        model = User
        fields = '__all__'

