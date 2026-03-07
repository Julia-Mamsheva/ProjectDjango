from django.urls import path
from . import views  # Импорт представлений из текущего приложения

# Пространство имен для URL-шаблонов приложения
# Позволяет использовать 'books:book_list' в шаблонах и представлениях
app_name = 'books'

# Список всех URL-маршрутов приложения
urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    # Пример использования в шаблоне: {% url 'books:home' %}
    
    # Список книг
    path('books/', views.book_list, name='book_list'),
    # Пример: /books/
    
    # Детальная страница книги (динамический параметр pk - первичный ключ)
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    # Пример: /books/1/ (просмотр книги с ID=1)
    # <int:pk> - конвертер, ожидает целое число и передает его в представление
    
    # Создание новой книги
    path('books/create/', views.book_create, name='book_create'),
    # Пример: /books/create/ (форма создания книги)
    
    # Редактирование существующей книги
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    # Пример: /books/1/update/ (редактирование книги с ID=1)
    
    # Удаление книги
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    # Пример: /books/1/delete/ (удаление книги с ID=1)
    
    # Список авторов
    path('authors/', views.author_list, name='author_list'),

    # Создание нового автора
    path('authors/create/', views.author_create, name='author_create'),

    # Детальная страница кроссовок
    path('sneaker/', views.sneaker_detail, name='sneaker_detail'),
    
]