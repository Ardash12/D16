from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_filters import FilterSet
from django.forms import ModelForm

from allauth.account.forms import SignupForm

from ads.models import Answer


class BaseRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.EmailField(label='Email')
    # first_name = forms.CharField(label="Имя")
    # last_Name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


class MyCustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        
        # Add your own processing here.

        # You must return the original result.
        return user