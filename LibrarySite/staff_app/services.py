import datetime as dt

from library.models import *
from library.services import STATUS_BORROW, STATUS_FREE, STATUS_LOST


class NotEnoughTextbooksError(Exception):
    pass


def issue_a_book(book_id, user_id):
    book_instance = BookInstance.objects.filter(book=book_id,
                                                status=Status.objects.get(id=STATUS_FREE))[0]
    book_instance.borrower = User.objects.get(id=user_id)
    book_instance.status = Status.objects.get(id=STATUS_BORROW)
    today = dt.date.today()
    book_instance.take_date = today + dt.timedelta(days=1)
    book_instance.return_date = today + dt.timedelta(days=8)
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

    list_authors = Author.objects.all().filter(id__in=list(map(int, authors)))
    for author in list_authors:
        new_book.author.add(author)

    add_instances_to_book(new_book, count)


def add_instances_to_book(book: Book, count: int):
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


def get_info():
    books = BookInstance.objects.all()
    free_books_count = books.filter(status=STATUS_FREE).count()
    issue_books_count = books.filter(status=STATUS_BORROW).count()
    textbooks = TextbookInstance.objects.all()
    free_textbooks_count = textbooks.filter(status=STATUS_FREE).count()
    issue_textbooks_count = textbooks.filter(status=STATUS_BORROW).count()
    return {'free_books_count': free_books_count, 'issue_books_count': issue_books_count,
            'free_textbooks_count': free_textbooks_count, 'issue_textbooks_count': issue_textbooks_count}
