from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
import logging

# подключение файла для логирования
logging.basicConfig(filename='views_logging.log',
                    format="%(asctime)s | %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


def page_not_found_view(request):
    # ,exception
    return render(request, '404.html', status=404)


def index(request):
    return render(request, 'index.html')


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
            if user.password == password:
                pass