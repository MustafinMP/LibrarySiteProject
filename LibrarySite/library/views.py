from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from .models import Book, Author, BookInstance
import logging
# подключение файла для логирования
logging.basicConfig(filename='views_logging.log',
                    format="%(asctime)s | %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


# ========================================= Функции представлений =========================================

# главная страница
def index(request):
    return render(request, 'index.html')


# страница с информацией о сайте
def about(request):
    return render(request, 'about.html')


# ------------------------------------------------- Книги -------------------------------------------------
def books_view(request):
    books = Book.objects.all()
    context = {'books': books, 'media': settings.STATIC_URL}
    return render(request, 'books.html', context=context)


def one_book(request, book_id):
    if request == 'POST':
        pass
    else:
        book = Book.objects.get(id=book_id)
        count = book.bookinstance_set.all().filter(status=1).count()
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


# ---------------------------------------------------------------------------------------------------------


# ------------------------------------------------- Авторы ------------------------------------------------
def authors_view(request):
    authors = Author.objects.all()
    context = {'authors': authors, 'media': settings.STATIC_URL}
    return render(request, 'authors.html', context=context)


def one_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = author.book.all()
    context = {'author': author, 'books': books}
    return render(request, 'one_author.html', context=context)


# ---------------------------------------------------------------------------------------------------------
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('username')
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            e_mail = request.POST.get('e_mail')
            password = request.POST.get('password')
            user = User.objects.create_user(username, e_mail, password)
            user.last_name = last_name
            user.first_name = name
            user.save()
            logging.info(f'created user "{username}"')
            return HttpResponsePermanentRedirect('login/')
    else:
        register_form = RegisterForm()
        return render(request, 'register.html', {'form': register_form})


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username)


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user2 = request.user
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
    if user == user2:
        return render(request, 'profile.html', context=context)


def page_not_found_view(request):
    # ,exception
    return render(request, '404.html', status=404)
