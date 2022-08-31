from django.shortcuts import render
from .forms import RegisterForm, LoginForm, AddNewBookForm, ChangePasswordForm, BooksFilterForm, \
    AddTextBookFromExcelForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from .models import Book, Author, BookInstance, Status, TextbookInstance, Textbook, Genre, PublishingHouse
from . import services
import openpyxl
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


# главная страница
def index(request):
    return render(request, 'index.html')


# страница с информацией о сайте
def about(request):
    return render(request, 'about.html')


'''   Book Views   '''


def books_view(request):
    page = request.GET.get('page', 1)
    books = services.get_books()
    context = {'books': books, 'media': settings.STATIC_URL}
    return render(request, 'books.html', context=context)


def book_homepage(request):
    classic_books_slice = services.get_books(genres=[11], count=4)  # wrong genre id
    all_books_slice = services.get_books(count=5)
    context = {'classic_books_slice': classic_books_slice, 'all_books_slice': all_books_slice}
    return render(request, 'book_homepage.html', context=context)


def catalog(request):
    page = request.GET.get('page', 1)
    genre = request.GET.get('genre', None)
    genres = Genre.objects.all()

    if genre:
        genre_label = genres.filter(id=genre)[0].title
        page = services.get_books_with_pagination(page=page, genres=[genre])
    else:
        genre_label = 'Все книги'
        page = services.get_books_with_pagination(page=page)
    context = {'page': page,
               'genres': genres,
               'genre_label': genre_label,
               'media': settings.STATIC_URL}
    return render(request, 'catalog.html', context=context)


def one_book(request, book_id):
    if request.method == 'POST':
        context = services.add_book_to_user(book_id, request.user)
        return render(request, 'one_book.html', context=context)
    else:
        book = Book.objects.get(id=book_id)
        count = book.bookinstance_set.all().filter(status=STATUS_FREE).count()
        user2 = request.user
        try:
            user_books = BookInstance.objects.get(borrower=user2)
            have_book = bool(user_books)
        except Exception:
            have_book = False
        return render(request, 'one_book.html', context={'book': book,
                                                         'count': count,
                                                         'have_book': have_book})


'''   Author Views   '''


def authors_view(request):
    authors = Author.objects.all()
    context = {'authors': authors, 'media': settings.STATIC_URL}
    return render(request, 'authors.html', context=context)


def one_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = author.book.all()
    context = {'author': author, 'books': books}
    return render(request, 'one_author.html', context=context)


'''   User Views   '''


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
        context = services.get_profile_info(user2)
        return render(request, 'profile.html', context=context)
    return render(request, 'not_your_profile.html')


def change_password_view(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                pwd = form.cleaned_data['password']
                conf_pwd = form.cleaned_data['confirm_password']
                if pwd == conf_pwd:
                    user.set_password(pwd)
                    user.save()
                    return render('request', 'change_password_complete.html')
        return render('request', 'change_password.html')
    return HttpResponsePermanentRedirect('/')


def page_not_found_view(request):
    # ,exception
    return render(request, '404.html', status=404)


'''   Staff Views   '''


def staff_index(request):
    return render(request, 'staff/index.html')


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


def staff_borrow_view(request):
    book_instances = BookInstance.objects.all().filter(status=STATUS_BORROW)
    today = datetime.date.today()
    context = {'book_instances': book_instances, 'today': today}
    return render(request, 'staff_borrow.html', context=context)


def staff_borrow_one_book(request, book_id):
    book_instance = BookInstance.objects.get(id=book_id)

    if request.method == 'POST':
        services.staff_borrow_book(book_instance, request.POST)
        return HttpResponsePermanentRedirect('/staff/borrow/')
    else:
        context = {'book_instance': book_instance}
        return render(request, 'staff_borrow_one_book.html', context=context)


def staff_borrow_textbook_view(request):
    textbook_instances = TextbookInstance.objects.all().filter(status=STATUS_BORROW)
    context = {'textbook_instances': textbook_instances}
    return render(request, 'staff_borrow_textbook.html', context=context)


def add_book(request):
    if request.method == 'POST':
        add_book_form = AddNewBookForm(request.POST)
        if add_book_form.is_valid():
            title = add_book_form.cleaned_data.get('title')
            authors = add_book_form.cleaned_data.get('authors')
            genre = add_book_form.cleaned_data.get('genre')
            image = add_book_form.cleaned_data.get('image')
            publishing_house = add_book_form.cleaned_data.get('publishing_house')
            year_of_publication = add_book_form.cleaned_data.get('year_of_publication')
            count = add_book_form.cleaned_data.get('count')

            services.add_book_with_instances(title, authors, genre, image, publishing_house, year_of_publication, count)

            return render(request, 'add_book_success.html')
    else:
        add_book_form = AddNewBookForm()
        return render(request, 'add_book.html', {'form': add_book_form, 'errors': ''})


def add_book_ins(request, book_id):
    if request.method == 'POST':
        count = request.POST.get('count')
        services.add_instances_to_book(book_id, count)
        return render(request, 'add_book_success.html')


def add_textbooks_from_excel(request):
    if request.method == 'POST':
        form = AddTextBookFromExcelForm(request.POST, request.FILES)
        file = request.FILES['file'].file
        wb = openpyxl.load_workbook(file)
        worksheet = wb.active
        for row in worksheet.iter_rows(0, worksheet.max_row):
            title = row[0].value
            authors = row[1].value
            genre = row[2].value
            pb_house = row[3].value
            year_of_publication = row[4].value
            print([title, authors, genre, pb_house, year_of_publication])
        return render(request, 'add_book_success.html')
    else:
        form = AddTextBookFromExcelForm()
        return render(request, 'add_textbooks_from_excel.html', context={'form': form})
        # for row in range(0, worksheet.max_row):
        #     for col in worksheet.iter_cols(0, worksheet.max_column)
