"""For app's logic"""
import datetime
import logging

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Book, BookInstance, StudentGroup, UserData, Status

# book statuses
STATUS_FREE = 1
STATUS_BORROW = 2
STATUS_LOST = 3
STATUS_RESERVE = 4

logging.basicConfig(filename='site_logging.log',
                    format="%(asctime)s | %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


def get_books(authors=None, genres=None, is_free=None, count=None):
    filter_kwargs = {}
    if not (authors is None):
        filter_kwargs['author__in'] = authors
    if not (genres is None):
        filter_kwargs['genre__in'] = genres
    if not (is_free is None):
        filter_kwargs['bookinstance__status'] = 1
    if filter_kwargs:
        books = Book.objects.filter(**filter_kwargs).order_by('id')
    else:
        books = Book.objects.all().order_by('id')
    if not (count is None):
        books = books[:count]
    return books


def get_user_profile(user: User):
    try:
        books = BookInstance.objects.all().filter(borrower=user)
        today = datetime.date.today()
        context = {'user_data': user,
                   'have_book': True,
                   'books': books,
                   'today': today}
    except Exception:
        context = {'user_data': user,
                   'have_book': False}
    return context


def get_books_with_pagination(page=1, authors=None, genres=None, is_free=None):
    book_list = get_books(authors=authors, genres=genres, is_free=is_free)
    paginator = Paginator(book_list, 30)  # 30 books in each page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return books


def create_user(username: str, e_mail: str, password: str, first_name: str, last_name: str, group: tuple[int, str]):
    s_group = StudentGroup.objects.get(level=group[0], letter=group[1])
    user = User.objects.create_user(username, e_mail, password)
    user.last_name = last_name
    user.first_name = first_name
    user.save()
    additional_user_data = UserData.objects.create(user=user, group=s_group, is_graduate=False)
    additional_user_data.save()
    logging.info(f'created user "{username}"')


def add_book_to_user(book_id, user):
    book_instance = BookInstance.objects.all().filter(status=STATUS_FREE, book=book_id)[0]
    book_instance.borrower = user
    book_instance.status = Status.objects.get(id=STATUS_RESERVE)
    book_instance.save()
    logging.info(f'user {user} reserved book {Book.objects.get(id=book_id).title}')
    book = Book.objects.get(id=book_id)
    count = book.bookinstance_set.all().filter(status=1).count()
    return {'book': book,
            'count': count,
            'have_book': True}