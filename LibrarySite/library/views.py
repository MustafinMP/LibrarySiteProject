import logging

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, reverse

from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .services import *

# подключение файла для логирования
logging.basicConfig(filename='site_logging.log',
                    format="%(asctime)s : %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


# главная страница
def index(request):
    return render(request, 'index.html')


# страница с информацией о сайте
def about(request):
    return render(request, 'about.html')


'''   Book Views   '''


def catalog(request):
    page = request.GET.get('page', 1)
    genre = request.GET.get('genre', None)
    genres = Genre.objects.all()

    if genre:
        genre_label = genres.filter(id=genre)[0].title
        page = get_books_with_pagination(page=page, genres=[genre])
    else:
        genre_label = 'Все книги'
        page = get_books_with_pagination(page=page)
    context = {'page': page,
               'genres': genres,
               'genre_label': genre_label,
               'media': settings.STATIC_URL}
    return render(request, 'catalog.html', context=context)


def book_item(request, book_id):
    book = Book.objects.get(id=book_id)
    count = book.bookinstance_set.all().filter(status=STATUS_FREE).count()
    user_from_request = request.user
    try:
        user_books = BookInstance.objects.get(borrower=user_from_request)
        have_book = bool(user_books)
    except Exception:
        have_book = False
    return render(request, 'book_item.html', context={'book': book,
                                                      'count': count,
                                                      'have_book': have_book})


'''   Author Views   '''


def authors_view(request):
    authors = Author.objects.all()
    context = {'authors': authors, 'media': settings.STATIC_URL}
    return render(request, 'authors.html', context=context)


def author_person_view(request, author_id):
    author = Author.objects.get(id=author_id)
    books = author.book.all()
    context = {'author': author, 'books': books}
    return render(request, 'author_person.html', context=context)


'''   User Views   '''


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            # получение данных из формы
            username = request.POST.get('username')
            first_name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            e_mail = request.POST.get('e_mail')
            password = request.POST.get('password')
            group = request.POST.get('group')
            try:
                # пробуем добавить нового юзера
                level = int(group[:-1])
                letter = group[-1].upper()
                create_user(username, e_mail, password, first_name, last_name, (level, letter))
            except Exception as e:
                # если данные некорректны, сообщаем об этом пользователю
                print(e)
                register_form.add_error('group', f'Класс {group} отсутствует в базе')
                return render(request, 'register.html', {'form': register_form})
            return HttpResponsePermanentRedirect(reverse('login_page'))
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
    user_from_request = request.user
    if not user_from_request.is_authenticated:
        return HttpResponsePermanentRedirect('/login')
    user = User.objects.get(id=user_id)
    if user_from_request == user:
        context = get_user_profile(user_from_request)
        return render(request, 'profile.html', context=context)
    return render(request, 'not_user_profile.html')


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


def exception404(request):
    # ,exception
    return render(request, '404.html', status=404)
