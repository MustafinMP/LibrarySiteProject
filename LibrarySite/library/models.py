from django.db import models
from django.contrib.auth.models import User

'''
All application models

Все модели приложения
'''

'''---------------------------------------------------------------------------------------------------------------------
Вспомогательные модели
---------------------------------------------------------------------------------------------------------------------'''


class Genre(models.Model):
    title = models.CharField(verbose_name='Жанр книги',
                             max_length=30
                             )

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(verbose_name='Статус книги',
                             max_length=20
                             )

    def __str__(self):
        return self.title


class PublishingHouse(models.Model):
    name = models.CharField(verbose_name='Издательство книги',
                            max_length=60
                            )

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    level = models.IntegerField(default=1)
    letter = models.CharField(max_length=1)

    def __str__(self):
        return f'{self.level}{self.letter}'


class AdditionalUserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    group = models.ForeignKey(StudentGroup, on_delete=models.PROTECT, blank=True, null=True)
    is_graduate = models.BooleanField()


'''---------------------------------------------------------------------------------------------------------------------
Основные модели
---------------------------------------------------------------------------------------------------------------------'''


class Author(models.Model):
    name = models.CharField(verbose_name='Имя',
                            max_length=30)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=100)
    book = None

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def display_book(self):
        return ', '.join([f'{book.title}' for book in self.book.all()])

    display_book.short_description = 'Книги'


'''---------------------------------------------------------------------------------------------------------------------
Книги и их экземпляры
---------------------------------------------------------------------------------------------------------------------'''


class Book(models.Model):
    title = models.CharField(verbose_name='Название книги',
                             max_length=100)
    genre = models.ForeignKey(Genre,
                              on_delete=models.PROTECT)
    author = models.ManyToManyField(Author,
                                    verbose_name='Авторы книги',
                                    related_name='book')
    image = models.ImageField(verbose_name='Изображение обложки книги',
                              upload_to='bookimg/')
    publishing_house = models.ForeignKey(PublishingHouse,
                                         verbose_name='Издательство',
                                         on_delete=models.PROTECT,
                                         blank=True,
                                         null=True)
    year_of_publication = models.IntegerField(verbose_name='Год публикации',
                                              blank=True,
                                              null=True)

    def __str__(self):
        return self.title

    def display_author(self):
        return ', '.join([f'{author.name} {author.last_name}' for author in self.author.all()])

    display_author.short_description = 'Авторы'

    @property
    def img_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class BookInstance(models.Model):
    """Класс экземпляра книги"""
    book = models.ForeignKey(Book,
                             verbose_name='Книга',
                             on_delete=models.PROTECT)
    status = models.ForeignKey(Status,
                               verbose_name='Статус экземпляра',
                               on_delete=models.PROTECT)
    take_date = models.DateField(verbose_name='Дата выдачи',
                                 blank=True,
                                 null=True)
    return_date = models.DateField(verbose_name='Дата возврата',
                                   blank=True,
                                   null=True)
    borrower = models.OneToOneField(User,
                                    verbose_name='Держатель экземпляра',
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True)

    def __str__(self):
        return f'{self.id}, {self.book}'


'''---------------------------------------------------------------------------------------------------------------------
Учебники и их экземпляры
---------------------------------------------------------------------------------------------------------------------'''


class Textbook(models.Model):
    title = models.CharField(verbose_name='Название учебника',
                             max_length=100)
    genre = models.ForeignKey(Genre,
                              on_delete=models.PROTECT)
    author = models.ManyToManyField(Author,
                                    verbose_name='Авторы учебника',
                                    related_name='textbook')
    image = models.ImageField(verbose_name='Изображение обложки учебника',
                              upload_to='textbookimg/')
    level = models.IntegerField()
    publishing_house = models.ForeignKey(PublishingHouse,
                                         verbose_name='Издательство',
                                         on_delete=models.PROTECT,
                                         blank=True,
                                         null=True)
    year_of_publication = models.IntegerField(verbose_name='Год публикации',
                                              blank=True,
                                              null=True)

    def __str__(self):
        return self.title

    def display_author(self):
        return ', '.join([f'{author.name} {author.last_name}' for author in self.author.all()])

    display_author.short_description = 'Авторы'

    @property
    def img_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class TextbookInstance(models.Model):
    textbook = models.ForeignKey(Textbook,
                                 verbose_name='Учебник',
                                 on_delete=models.PROTECT,
                                 related_name='textbook',
                                 blank=True,
                                 null=True)
    status = models.ForeignKey(Status,
                               verbose_name='Статус учебника',
                               on_delete=models.PROTECT)
    borrower = models.ForeignKey(User,
                                 verbose_name='Держатель учебника',
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True)

    def __str__(self):
        return f'{self.id}, {self.textbook}'


'''------------------------------------------------------------------------------------------------------------------'''
