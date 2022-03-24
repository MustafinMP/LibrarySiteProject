from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Status, Textbook, TextbookInstance, PublishingHouse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Genre)
# admin.site.register(Status)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'borrower')


@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'publishing_house')


@admin.register(TextbookInstance)
class TextbookInstanceAdmin(admin.ModelAdmin):
    list_display = ('textbook', 'status', 'borrower')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    pass
