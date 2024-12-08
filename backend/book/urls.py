from django.urls import path
from .views import create_book_view, book_list_view, book_detail_view

urlpatterns = [
    path('publish', create_book_view, name='book-upload'),
    path('list', book_list_view, name='book-list'),
    path('<int:book_id>', book_detail_view, name='book-detail'),
]
