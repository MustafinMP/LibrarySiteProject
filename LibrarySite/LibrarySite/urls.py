"""LibrarySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from library import views

urlpatterns = [
                  path('',
                       views.index),
                  path('admin/',
                       admin.site.urls),
                  path('about/',
                       views.about),

                  path('books/',
                       views.books_view),
                  path('books/<int:book_id>/',
                       views.one_book),

                  path('authors/',
                       views.authors_view),
                  path('authors/<int:author_id>/', views.one_author),

                  path('accounts/',
                       include('django.contrib.auth.urls')),
                  path('register/',
                       views.register),
                  path('profile/<int:user_id>/',
                       views.profile),
                  path('login/',
                       views.login_view),
                  path('logout/',
                       auth_views.LogoutView.as_view(),
                       {'next_page': settings.LOGOUT_REDIRECT_URL},
                       name='logout'),

                  path('staff/reserve/',
                       views.staff_reserve),
                  path('staff/reserve/<book_id>/',
                       views.staff_reserve_one_book),
                  path('staff/borrow/',
                       views.staff_borrow),
                  path('staff/borrow/<book_id>/',
                       views.staff_borrow_one_book),
                  path('staff/borrow-textbook/',
                       views.staff_borrow_textbook),

                  path('404testing/',
                       views.page_not_found_view),

              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)

# handler404 = "library.views.page_not_found_view"
