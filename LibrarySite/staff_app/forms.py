from django import forms
from ..library.models import Author, Genre, PublishingHouse, Book, Textbook, StudentGroup, User

genres = Genre.objects.all()
authors = Author.objects.all()
pbhs = PublishingHouse.objects.all()


def get_users():
    users = User.objects.all()
    return [(user.id, f'{str(user.userdata.group)} {user.first_name} {user.last_name}') for user in users]


def get_authors():
    authors = Author.objects.all()


def get_groups():
    groups = StudentGroup.objects.all()
    return [(groups[i].id, str(groups[i])) for i in range(len(groups))]


def get_genres():
    genres = Genre.objects.all()
    return [(genres[i].id, genres[i].title) for i in range(len(genres))]


def get_books():
    books = Book.objects.all()
    return [(books[i].id, books[i].title) for i in range(len(books))]


def get_textbooks():
    textbooks = Textbook.objects.all()
    return [(textbooks[i].id,
             f'{textbooks[i].level} класс "{textbooks[i].title}" ' +
             f'{textbooks[i].display_one_author()}, {textbooks[i].year_of_publication}')
            for i in range(len(textbooks))]


class AddNewBookForm(forms.Form):
    title = forms.CharField(label='Название книги', help_text='Введите название книги')
    authors = forms.TypedMultipleChoiceField(label='Автор(ы)',
                                             choices=([(authors[i].id, authors[i]) for i in range(len(authors))]))
    genre = forms.TypedChoiceField(label='Жанр', choices=(get_genres()))
    image = forms.ImageField(label='Обложка книги (можно добавить позже)', required=False, )
    count = forms.IntegerField(label='Количество экземпляров книги', initial=1)
    publishing_house = forms.TypedChoiceField(label='Издательство',
                                              choices=([(pbhs[i].id, pbhs[i]) for i in range(len(pbhs))]))
    year_of_publication = forms.IntegerField()


class AddTextBookFromExcelForm(forms.Form):
    file = forms.FileField()


class AddNewBookInstanceForm(forms.Form):
    book = forms.TypedChoiceField(label='Книга', choices=(get_books()))
    count = forms.IntegerField(label='Количество экземпляров книги', initial=1)


class IssueTextbookForm(forms.Form):
    textbook = forms.TypedChoiceField(label='Учебник', choices=(get_textbooks()))
    group = forms.TypedChoiceField(label='Класс', choices=(get_groups()))
    borrower = forms.CharField()


class IssueABookForm(forms.Form):
    borrower = forms.TypedChoiceField(label='Получатель', choices=(get_users()))
