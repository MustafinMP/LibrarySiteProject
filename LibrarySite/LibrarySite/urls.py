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
                  path('', views.index, name='homepage'),
                  path('admin/', admin.site.urls),
                  path('about/', views.about),

                  path('catalog/', views.catalog),

                  path('catalog/<int:book_id>/', views.book_item),

                  path('authors/', views.authors_view),
                  path('authors/<int:author_id>/', views.author_person),

                  path('profile/<int:user_id>/', views.profile),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('register/', views.register),
                  path('login/', views.login_view, name='login_page'),
                  path('logout/', auth_views.LogoutView.as_view(),
                       {'next_page': settings.LOGOUT_REDIRECT_URL},
                       name='logout'),
                  path('change_password', views.change_password_view),

                  path('staff/', views.Staff.index),

                  path('staff/borrow/', views.Staff.borrow_view, name='borrow_page'),
                  path('staff/borrow/<book_id>/', views.Staff.borrow_one_book),
                  path('staff/borrow-textbook/', views.Staff.borrow_textbook_view),

                  path('staff/add_book/', views.Staff.add_book),
                  path('staff/add_book_ins/', views.Staff.add_book_ins),
                  path('staff/add_textbooks_from_excel/', views.Staff.add_textbooks_from_excel),

                  path('staff/issue_books', views.Staff.issue_books),
                  path('staff/issue_a_book/<book_id>/', views.Staff.issue_a_book),

                  path('staff/issue_textbooks/', views.Staff.issue_textbooks),
                  path('staff/issue_textbooks_list/', views.Staff.issue_textbooks_list),

                  path('exception404/', views.exception404),

              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)

# handler404 = "library.views.page_not_found_view"
