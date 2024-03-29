import datetime as dt

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, reverse

from library.services import get_books_with_pagination
from .forms import AddNewBookForm, AddNewBookInstanceForm, IssueTextbookForm, \
    IssueABookForm
from .services import *


def staff_only(func):
    """Проверка доступа"""

    def wrapper(*args, **kwargs):
        if args[0].user.is_staff:
            return func(*args, **kwargs)
        return HttpResponsePermanentRedirect('/')

    return wrapper


@staff_only
def index(request):
    return render(request, 'staff/index.html', context=get_info())


@staff_only
def issue_books_view(request):
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
               'media': settings.STATIC_URL,
               'mode': 'staff'}
    return render(request, 'catalog.html', context=context)


@staff_only
def issue_a_book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    count = book.bookinstance_set.all().filter(status=STATUS_FREE).count()
    if request.method == 'POST':
        issue_a_book_form = IssueABookForm(request.POST)
        if issue_a_book_form.is_valid():
            user_id = issue_a_book_form.cleaned_data.get('borrower')
            issue_a_book(book_id, user_id)
            return HttpResponsePermanentRedirect(reverse('borrow_page'))
    else:
        issue_a_book_form = IssueABookForm()
        context = {'book': book, 'count': count, 'form': issue_a_book_form}
        return render(request, 'staff/issue_a_book.html', context=context)


@staff_only
def borrow_view(request):
    book_instances = BookInstance.objects.all().filter(status=STATUS_BORROW)
    today = dt.date.today()
    context = {'book_instances': book_instances, 'today': today}
    return render(request, 'staff/borrow.html', context=context)


@staff_only
def borrow_one_book_view(request, book_id):
    book_instance = BookInstance.objects.get(id=book_id)

    if request.method == 'POST':
        staff_borrow_book(book_instance, request.POST)
        return HttpResponsePermanentRedirect('/staff/borrow/')
    today = dt.date.today()
    context = {'book_instance': book_instance, 'today': today}
    return render(request, 'staff/borrow_one_book.html', context=context)


@staff_only
def borrow_textbook_view(request):
    textbook_instances = TextbookInstance.objects.all().filter(status=STATUS_BORROW)
    context = {'textbook_instances': textbook_instances}
    return render(request, 'staff/borrow_textbook.html', context=context)


@staff_only
def add_book_view(request):
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

            add_book_with_instances(title, authors, genre, image, publishing_house,
                                    year_of_publication,
                                    count)
            return render(request, 'staff/add_book_success.html')
    add_book_form = AddNewBookForm()
    return render(request, 'staff/add_book.html', {'form': add_book_form, 'errors': ''})


@staff_only
def add_book_instance_view(request):
    if request.method == 'POST':
        add_book_form = AddNewBookInstanceForm(request.POST)
        if add_book_form.is_valid():
            count = int(request.POST.get('count'))
            book_id = int(request.POST.get('book'))
            book = Book.objects.get(id=book_id)
            add_instances_to_book(book, count)
            return render(request, 'staff/add_book_success.html')
    else:
        add_book_form = AddNewBookInstanceForm()
        return render(request, 'staff/add_book_ins.html', {'form': add_book_form, 'errors': ''})


@staff_only
def issue_textbooks_view(request):
    if request.method == 'POST':
        form = IssueTextbookForm(request.POST)
        if form.is_valid():
            textbook = form.cleaned_data['textbook']
            group = form.cleaned_data['group']
            borrower = form.cleaned_data['borrower']
            try:
                issue_textbooks(textbook, group, borrower)
            except NotEnoughTextbooksError:
                return
            return HttpResponsePermanentRedirect('/')
        return render(request, 'staff/issue_textbooks.html', context={'text': 'error', 'form': form})
    form = IssueTextbookForm()
    return render(request, 'staff/issue_textbooks.html', context={'text': 'text', 'form': form})


@staff_only
def issue_textbooks_list_view(request):
    textbooks = IssueTextbooks.objects.all()
    return render(request, 'staff/issued_textbook_list.html', context={'textbooks': textbooks})

@staff_only
def reserve(request):
        if request.user.is_staff:
            book_instances = BookInstance.objects.all().filter(status=STATUS_RESERVE)
            context = {'book_instances': book_instances}
            return render(request, 'staff/reserve.html', context=context)
        return HttpResponsePermanentRedirect('/')

@staff_only
def reserve_one_book(request, book_id):
        if request.user.is_staff:
            book_instance = BookInstance.objects.get(id=book_id)

            if request.method == 'POST':
                if '_approve' in request.POST:
                    book_instance.status = Status.objects.get(id=STATUS_BORROW)
                    today = dt.date.today()
                    book_instance.take_date = today + dt.timedelta(days=1)
                    book_instance.return_date = today + dt.timedelta(days=8)

                elif '_reject' in request.POST:
                    book_instance.status = Status.objects.get(id=STATUS_FREE)
                    book_instance.borrower = None

                book_instance.save()
                return HttpResponsePermanentRedirect('/staff/reserve/')
            context = {'book_instance': book_instance}
            return render(request, 'staff/reserve_one_book.html', context=context)
        return HttpResponsePermanentRedirect('/')