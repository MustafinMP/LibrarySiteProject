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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

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
                  path('change_password/', views.change_password_view),

                  path('staff/', include('staff_app.urls'))

              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = "library.views.page_not_found_view"
