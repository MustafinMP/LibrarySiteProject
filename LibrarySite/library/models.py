from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

'''
All application models

Все модели приложения
'''


# ----------------- Вспомогательные модели -----------------
class Genre(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='Жанр книги'
    )

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Статус книги'
    )

    def __str__(self):
        return self.title


class PublishingHouse(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Издательство книги'
    )

    def __str__(self):
        return self.name


# -------------------------------------------------------------


# ---------------------- Основные модели ----------------------
class Author(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    book = None

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def display_book(self):
        return ', '.join([f'{book.title}' for book in self.book.all()])

    display_book.short_description = 'Книги'


# --------------------- Книги и их экземпляры --------------------------
class Book(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название книги'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT
    )
    author = models.ManyToManyField(Author, related_name='book')
    image = models.ImageField(
        verbose_name='Изображение обложки книги',
        upload_to='bookimg/'
    )
    publishing_house = models.ForeignKey(
        PublishingHouse,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    year_of_publication = models.IntegerField(
        blank=True,
        null=True
    )

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
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT
    )
    take_date = models.DateField(
        verbose_name='Дата выдачи',
        blank=True,
        null=True
    )
    return_date = models.DateField(
        verbose_name='Дата возврата',
        blank=True,
        null=True
    )
    borrower = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.id}, {self.book}'


# ---------------------------------------------------------------------------------


# ------------------------- Учебники и их экземпляры -----------------------------------
class Textbook(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название учебника'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT
    )
    author = models.ManyToManyField(
        Author,
        related_name='textbook')
    image = models.ImageField(
        verbose_name='Изображение обложки учебника',
        upload_to='textbookimg/'
    )
    level = models.IntegerField(
    )
    publishing_house = models.ForeignKey(
        PublishingHouse,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    year_of_publication = models.IntegerField(
        blank=True,
        null=True
    )

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
    textbook = models.ForeignKey(
        Textbook,
        on_delete=models.PROTECT,
        related_name='textbook',
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT
    )
    borrower = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.id}, {self.textbook}'
# ------------------------------------------------------------------------------
