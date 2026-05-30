from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StudentRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    branch = forms.CharField(max_length=100)

    year = forms.CharField(max_length=20)

    

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class StaffRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )