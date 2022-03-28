from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='логин',
        help_text='''Введите свой логин'''
    )
    name = forms.CharField(
        label='Имя:',
        help_text='Введите Ваше имя'
    )
    last_name = forms.CharField(
        label='Фамилия:',
        help_text='Введите Вашу фамилию'
    )
    e_mail = forms.EmailField(
        label='Email:',
        help_text='Введите Вашу электронную почту'
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput,
        help_text='Введите пароль'
    )


class LoginForm(forms.Form):
# class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Введите имя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Введите пароль'
    )
