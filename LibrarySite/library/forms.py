from django import forms
from .models import Author, Genre, PublishingHouse

genres = Genre.objects.all()
authors = Author.objects.all()
pbhs = PublishingHouse.objects.all()


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин',
                               help_text='''Введите свой логин''')

    name = forms.CharField(label='Имя:',
                           help_text='Введите Ваше имя')

    last_name = forms.CharField(label='Фамилия:',
                                help_text='Введите Вашу фамилию')

    e_mail = forms.EmailField(label='Email:',
                              help_text='Введите Вашу электронную почту')

    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput,
                               help_text='Введите пароль')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин',
                               help_text='Введите свой логин'
                               )
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Пароль',
                               help_text='Введите пароль'
                               )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Пароль',
                               help_text='Введите новый пароль'
                               )
    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       label='Подтверждение пароля',
                                       help_text='Подтвердите новый пароль'
                                       )


class BooksFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genres_list = Genre.objects.all()
        for i in range(len(genres_list)):
            field = forms.BooleanField(label=genres_list[i].title)
            self.fields[f'genre_{i}'] = field
        print(self.fields)

    def get_genre_fields(self):
        for field_name in self.fields:
            if field_name.startswith('genre_'):
                yield self[field_name]

    def clean_filters(self):
        i = 0
        field_name = f'genre_{i}'
        genres_from_filter = []
        while self.cleaned_data.get(field_name):
            if self.cleaned_data[field_name]:
                genres_from_filter.append(i)
                i += 1
                field_name = f'genre_{i}'
        self.cleaned_data['filtered_genres'] = genres_from_filter


class AddNewBookForm(forms.Form):
    title = forms.CharField(label='Название книги',
                            help_text='Введите название книги'
                            )
    authors = forms.TypedMultipleChoiceField(label='Автор(ы)',
                                             choices=(
                                                 [(authors[i].id, authors[i]) for i in range(len(authors))]
                                             ))
    genre = forms.TypedChoiceField(label='Жанр',
                                   choices=(
                                       [(genres[i].id, genres[i].title) for i in range(len(genres))]
                                   ))
    image = forms.ImageField(label='Обложка книги (можно добавить позже)', required=False)
    count = forms.IntegerField(label='Количество экземпляров книги', initial=1)
    publishing_house = forms.TypedChoiceField(label='Жанр',
                                              choices=(
                                                  [(pbhs[i].id, pbhs[i]) for i in range(len(pbhs))]
                                              ))
    year_of_publication = forms.IntegerField()
