from django import forms

from library.models import Author, Genre, PublishingHouse, Book, Textbook, StudentGroup, User


def users():
    return [(user.id, f'{str(user.userdata.group)} {user.first_name} {user.last_name}') for user in User.objects.all()]


def authors():
    return [(author.id, author) for author in Author.objects.all()]


def groups():
    return [(group.id, str(group)) for group in StudentGroup.objects.all()]


def genres():
    return [(genre.id, genre.title) for genre in Genre.objects.all()]


def books():
    return [(book.id, book.title) for book in Book.objects.all()]


def textbooks():
    return [(textbook.id,
             f'{textbook.level} класс "{textbook.title}" ' +
             f'{textbook.display_one_author()}, {textbook.year_of_publication}')
            for textbook in Textbook.objects.all()]


def publishing_houses():
    return [(pbh.id, pbh) for pbh in PublishingHouse.objects.all()]


class AddNewBookForm(forms.Form):
    title = forms.CharField(label='Название книги', help_text='Введите название книги')
    authors = forms.TypedMultipleChoiceField(label='Автор(ы)',
                                             choices=(authors()))
    genre = forms.TypedChoiceField(label='Жанр', choices=(genres()))
    image = forms.ImageField(label='Обложка книги (можно добавить позже)', required=False, )
    count = forms.IntegerField(label='Количество экземпляров книги', initial=1)
    publishing_house = forms.TypedChoiceField(label='Издательство',
                                              choices=(publishing_houses()))
    year_of_publication = forms.IntegerField(label='Год выпуска')


class AddTextBookFromExcelForm(forms.Form):
    file = forms.FileField()


class AddNewBookInstanceForm(forms.Form):
    book = forms.TypedChoiceField(label='Книга', choices=(books()))
    count = forms.IntegerField(label='Количество экземпляров книги', initial=1)


class IssueTextbookForm(forms.Form):
    textbook = forms.TypedChoiceField(label='Учебник', choices=(textbooks()))
    group = forms.TypedChoiceField(label='Класс', choices=(groups()))
    borrower = forms.CharField(label='Получатель')


class IssueABookForm(forms.Form):
    borrower = forms.TypedChoiceField(label='Получатель', choices=(users()))
