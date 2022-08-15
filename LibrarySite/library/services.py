"""For app's logic"""

from .models import Book, Author, BookInstance, Status, TextbookInstance, Textbook, Genre, PublishingHouse


# user functions

def get_profile_info(user):
    try:
        book_ins = BookInstance.objects.get(borrower=user)
        book = book_ins.book
        context = {'user_data': user,
                   'have_book': True,
                   'book': book,
                   'book_ins': book_ins}
    except Exception:
        context = {'user_data': user,
                   'have_book': False}

    return context


def get_books(authors=None, genres=None, is_free=None):
    filter_kwargs = {}
    if not (authors is None):
        filter_kwargs['author__in'] = authors
    if not (genres is None):
        filter_kwargs['genre__in'] = genres
    if not (authors is None):
        filter_kwargs['bookinstance__status'] = 1
    if filter_kwargs:
        books = Book.objects.filter(**filter_kwargs)
    else:
        books = Book.objects.all()
    return books


