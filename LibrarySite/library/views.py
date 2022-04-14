from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from .models import Book, Author, BookInstance, Status, TextbookInstance, Textbook
import datetime
import logging

STATUS_FREE = 1
STATUS_BORROW = 2
STATUS_LOST = 3
STATUS_RESERVE = 4
# подключение файла для логирования
logging.basicConfig(filename='site_logging.log',
                    format="%(asctime)s | %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)

'''=====================================================================================================================
Функции представлений
====================================================================================================================='''


# главная страница
def index(request):
    return render(request, 'index.html')


# страница с информацией о сайте
def about(request):
    return render(request, 'about.html')


'''---------------------------------------------------------------------------------------------------------------------
Книги 
---------------------------------------------------------------------------------------------------------------------'''


def books_view(request):
    books = Book.objects.all()
    context = {'books': books, 'media': settings.STATIC_URL}
    return render(request, 'books.html', context=context)


def one_book(request, book_id):
    if request.method == 'POST':
        user = request.user
        book_instance = BookInstance.objects.all().filter(status=STATUS_FREE, book=book_id)[0]
        book_instance.borrower = user
        book_instance.status = Status.objects.get(id=STATUS_RESERVE)
        book_instance.save()
        logging.info(f'user {user} reserved book {Book.objects.get(id=book_id).title}')
        book = Book.objects.get(id=book_id)
        count = book.bookinstance_set.all().filter(status=1).count()
        return render(request, 'one_book.html', context={
            'book': book,
            'count': count,
            'have_book': True
        })
    else:
        book = Book.objects.get(id=book_id)
        count = book.bookinstance_set.all().filter(status=STATUS_FREE).count()
        user2 = request.user
        try:
            user_books = BookInstance.objects.get(borrower=user2)
            have_book = bool(user_books)
        except Exception:
            have_book = False
        return render(request, 'one_book.html', context={
            'book': book,
            'count': count,
            'have_book': have_book
        })


'''---------------------------------------------------------------------------------------------------------------------
Авторы
---------------------------------------------------------------------------------------------------------------------'''


def authors_view(request):
    authors = Author.objects.all()
    context = {'authors': authors, 'media': settings.STATIC_URL}
    return render(request, 'authors.html', context=context)


def one_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = author.book.all()
    context = {'author': author, 'books': books}
    return render(request, 'one_author.html', context=context)


'''---------------------------------------------------------------------------------------------------------------------
Действия с пользователем
---------------------------------------------------------------------------------------------------------------------'''


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            # получение данных из формы
            username = request.POST.get('username')
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            e_mail = request.POST.get('e_mail')
            password = request.POST.get('password')

            # создание пользователя
            user = User.objects.create_user(username, e_mail, password)
            user.last_name = last_name
            user.first_name = name
            user.save()

            logging.info(f'created user "{username}"')
            return HttpResponsePermanentRedirect('login/')
    else:
        register_form = RegisterForm()
        return render(request, 'register.html', {'form': register_form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                logging.info(f'login user "{username}"')
                return HttpResponsePermanentRedirect('/')

            else:
                login_form = LoginForm()
                return render(request, 'login.html', {'form': login_form, 'errors': 'Неверный пароль'})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form, 'errors': ''})


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user2 = request.user
    if user == user2:
        try:
            book_ins = BookInstance.objects.get(borrower=user2)
            book = book_ins.book
            have_book = True
            context = {
                'user_data': user,
                'have_book': have_book,
                'book': book,
                'book_ins': book_ins
            }
        except Exception:
            have_book = False
            context = {
                'user_data': user,
                'have_book': have_book
            }

        return render(request, 'profile.html', context=context)

    return render(request, 'not_your_profile.html')


def page_not_found_view(request):
    # ,exception
    return render(request, '404.html', status=404)


'''---------------------------------------------------------------------------------------------------------------------
Представления персонала
---------------------------------------------------------------------------------------------------------------------'''


def staff_reserve(request):
    book_instances = BookInstance.objects.all().filter(status=STATUS_RESERVE)
    context = {'book_instances': book_instances}
    return render(request, 'staff_reserve.html', context=context)


def staff_reserve_one_book(request, book_id):
    book_instance = BookInstance.objects.get(id=book_id)

    if request.method == 'POST':
        if '_approve' in request.POST:
            book_instance.status = Status.objects.get(id=STATUS_BORROW)
            today = datetime.date.today()
            book_instance.take_date = today + datetime.timedelta(days=1)
            book_instance.return_date = today + datetime.timedelta(days=8)

        elif '_reject' in request.POST:
            book_instance.status = Status.objects.get(id=STATUS_FREE)
            book_instance.borrower = None

        book_instance.save()
        return HttpResponsePermanentRedirect('/staff/reserve/')
    else:
        context = {'book_instance': book_instance}
        return render(request, 'staff_reserve_one_book.html', context=context)


def staff_borrow(request):
    book_instances = BookInstance.objects.all().filter(status=STATUS_BORROW)
    today = datetime.date.today()
    context = {'book_instances': book_instances, 'today': today}
    return render(request, 'staff_borrow.html', context=context)


def staff_borrow_one_book(request, book_id):
    book_instance = BookInstance.objects.get(id=book_id)

    if request.method == 'POST':
        if '_return' in request.POST:
            book_instance.status = Status.objects.get(id=STATUS_FREE)
            book_instance.borrower = None
            book_instance.take_date = None
            book_instance.return_date = None

        elif '_lost' in request.POST:
            book_instance.status = Status.objects.get(id=STATUS_LOST)
            book_instance.take_date = None
        # при утере книги пользователь теряет возможность получить новую книгу на 10 дней
            today = datetime.date.today()
            book_instance.return_date = today + datetime.timedelta(days=10)

        book_instance.save()
        return HttpResponsePermanentRedirect('/staff/borrow/')
    else:
        context = {'book_instance': book_instance}
        return render(request, 'staff_borrow_one_book.html', context=context)


def staff_borrow_textbook(request):
    textbook_instances = TextbookInstance.objects.all().filter(status=STATUS_BORROW)
    print(textbook_instances)
    context = {'textbook_instances': textbook_instances}
    return render(request, 'staff_borrow_textbook.html', context=context)