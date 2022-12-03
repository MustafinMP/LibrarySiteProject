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
                  path('authors/<int:author_id>/', views.author_person_view),

                  path('profile/<int:user_id>/', views.profile),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('register/', views.register),
                  path('login/', views.login_view, name='login_page'),
                  path('logout/', auth_views.LogoutView.as_view(),
                       {'next_page': settings.LOGOUT_REDIRECT_URL},
                       name='logout'),
                  path('change_password', views.change_password_view),

                  path('staff/', views.StaffViews.index),

                  path('staff/borrow/', views.StaffViews.borrow_view, name='borrow_page'),
                  path('staff/borrow/<book_id>/', views.StaffViews.borrow_one_book_view),
                  path('staff/borrow-textbook/', views.StaffViews.borrow_textbook_view),

                  path('staff/add_book/', views.StaffViews.add_book_view),
                  path('staff/add_book_ins/', views.StaffViews.add_book_instance_view),
                  path('staff/add_textbooks_from_excel/', views.StaffViews.add_textbooks_from_excel_view),

                  path('staff/issue_books', views.StaffViews.issue_books_view),
                  path('staff/issue_a_book/<book_id>/', views.StaffViews.issue_a_book_view),

                  path('staff/issue_textbooks/', views.StaffViews.issue_textbooks_view),
                  path('staff/issue_textbooks_list/', views.StaffViews.issue_textbooks_list_view),

                  path('exception404/', views.exception404),

              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = "library.views.page_not_found_view"
