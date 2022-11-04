"""For app's logic"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Book, Author, BookInstance, Status, TextbookInstance, Textbook, Genre, PublishingHouse, \
    StudentGroup, IssueTextbooks
import openpyxl
import logging
import datetime

# book statuses
STATUS_FREE = 1
STATUS_BORROW = 2
STATUS_LOST = 3

logging.basicConfig(filename='site_logging.log',
                    format="%(asctime)s | %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


class NotEnoughTextbooksError(Exception):
    pass


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


def get_user_profile(user):
    try:
        book_ins = BookInstance.objects.all().filter(borrower=user)[0]
        book = book_ins.book
        context = {'user_data': user,
                   'have_book': True,
                   'book': book,
                   'book_ins': book_ins}
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


# staff functions
def issue_a_book(book_id, user_id):
    book_instance = BookInstance.objects.filter(book=book_id,
                                                status=Status.objects.get(id=STATUS_FREE))[0]
    book_instance.borrower = User.objects.get(id=user_id)
    book_instance.status = Status.objects.get(id=STATUS_BORROW)
    today = datetime.date.today()
    book_instance.take_date = today + datetime.timedelta(days=1)
    book_instance.return_date = today + datetime.timedelta(days=8)
    book_instance.save()


def staff_borrow_book(book_instance, post_request):
    if '_return' in post_request:
        book_instance.status = Status.objects.get(id=STATUS_FREE)
        book_instance.borrower = None
        book_instance.take_date = None
        book_instance.return_date = None

    elif '_lost' in post_request:
        book_instance.status = Status.objects.get(id=STATUS_LOST)
        book_instance.take_date = None
    book_instance.save()


def add_book_with_instances(title, authors, genre, image, publishing_house, year_of_publication, count):
    new_book = Book.objects.create(title=title,
                                   genre=Genre.objects.all().filter(id=int(genre))[0],
                                   image=image,
                                   publishing_house=PublishingHouse.objects.all().filter(id=int(publishing_house))[0],
                                   year_of_publication=year_of_publication)
    new_book.save()

    # add authors
    list_authors = Author.objects.all().filter(id__in=list(map(int, authors)))
    for author in list_authors:
        new_book.author.add(author)

    add_instances_to_book(new_book, count)


def add_instances_to_book(book, count):
    for _ in range(count):
        book_instance = BookInstance.objects.create(book=book,
                                                    status=Status.objects.get(id=STATUS_FREE))


def issue_textbooks(textbook, group, borrower):
    textbook = Textbook.objects.get(id=textbook)
    group_user = User.objects.all().filter(user_data__group__id=group)
    group = StudentGroup.objects.get(id=group)
    count = len(group_user)
    textbook_instances = TextbookInstance.objects.all().filter(status=STATUS_FREE)
    if len(textbook_instances) < count:
        raise NotEnoughTextbooksError
    for i in range(count):
        tb = textbook_instances[i]
        tb.borrower = group_user[i]
        tb.status = Status.objects.get(id=STATUS_BORROW)
        tb.save()
    issue_tbs = IssueTextbooks.objects.create(textbook=textbook, group=group, count=count, borrower=borrower)
    issue_tbs.save()
