from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            e_mail = request.POST.get('e_mail')
            password = request.POST.get('password')
            user = User.objects.create_user(name, e_mail, password)
            user.last_name = last_name
            user.save()
            return  # TODO: завершить возврат формы
    else:
        register_form = RegisterForm()
        return render(request, 'register.html', {'form': register_form})
