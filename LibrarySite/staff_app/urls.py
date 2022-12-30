from django.urls import path
from . import views

app_name = "staff_app"

urlpatterns = [
    path('', views.index),

    path('borrow/', views.borrow_view, name='borrow_page'),
    path('borrow/<book_id>/', views.borrow_one_book_view),
    path('borrow-textbook/', views.borrow_textbook_view),

    path('add_book/', views.add_book_view),
    path('add_book_ins/', views.add_book_instance_view),
    path('add_textbooks_from_excel/', views.add_textbooks_from_excel_view),

    path('issue_books', views.issue_books_view),
    path('issue_a_book/<book_id>/', views.issue_a_book_view),

    path('issue_textbooks/', views.issue_textbooks_view),
    path('issue_textbooks_list/', views.issue_textbooks_list_view),
]
