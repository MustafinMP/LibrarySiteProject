from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label='Имя:',
                           help_text='Введите Ваше имя')
    last_name = forms.CharField(label='Фамилия:',
                                help_text='Введите Вашу фамилию')
    e_mail = forms.EmailField(label='Email:',
                              help_text='Введите Вашу электронную почту')
    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput,
                               help_text='Введите пароль')
