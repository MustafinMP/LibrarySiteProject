from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    title = models.CharField(max_length=30,
                             verbose_name='Жанр книги')

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=20,
                             verbose_name='Статус книги')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name='Имя')
    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия')

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Название книги')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    author = models.ManyToManyField(Author)
    image = models.ImageField(verbose_name='Изображение обложки книги',
                              upload_to='bookimg/')

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
    book = models.ForeignKey(Book,
                             on_delete=models.PROTECT)
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT)
    take_date = models.DateField(verbose_name='Дата выдачи',
                                 blank=True)
    return_date = models.DateField(verbose_name='Дата возврата',
                                   blank=True)
    borrower = models.OneToOneField(User,
                                    on_delete=models.PROTECT,
                                    blank=True)

    def __str__(self):
        return f'{self.id}, {self.book}'
