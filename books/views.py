# Create your views here.
# Импорт необходимых модулей и классов
from django.shortcuts import render, get_object_or_404, redirect  # Утилиты для работы с представлениями
from django.db.models import Q  # Для сложных запросов с OR (логическое ИЛИ)
from django.contrib import messages  # Для отображения уведомлений пользователю
from .models import Book, Author  # Модели данных
from .forms import BookForm, AuthorForm, BookSearchForm  # Формы


# Главная страница - вывод статистики и информации
def home(request):
    """
    Главная страница приложения.
    Отображает общую статистику по библиотеке:
    - общее количество книг
    - общее количество авторов
    - количество доступных книг
    - последние 5 добавленных книг
    """
    # Подсчет количества записей в базе данных
    total_books = Book.objects.count()  # Все книги
    total_authors = Author.objects.count()  # Все авторы
    available_books = Book.objects.filter(is_available=True).count()  # Только доступные
    recent_books = Book.objects.all()[:5]  # Последние 5 книг (сортировка по умолчанию - по дате создания)
    
    # Контекст для передачи в шаблон
    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'available_books': available_books,
        'recent_books': recent_books,
    }
    return render(request, 'books/home.html', context)


# ВНИМАНИЕ: Возможно, этот view относится к другому приложению
def sneaker_detail(request):
    """
    Отображает страницу с деталями кроссовок.
    Вероятно, этот view должен быть в другом приложении или это ошибка.
    """
    return render(request, 'books/sneaker_detail.html')


# Список книг с фильтрацией и поиском
def book_list(request):
    """
    Отображает список всех книг с возможностью фильтрации.
    Использует BookSearchForm для получения параметров фильтрации.
    Оптимизирован с select_related для уменьшения количества запросов к БД.
    """
    # Получаем все книги с предварительной загрузкой связанных авторов
    # select_related уменьшает количество запросов к БД при обращении к book.author
    books = Book.objects.select_related('author').all()
    
    # Инициализируем форму с GET параметрами (из URL)
    form = BookSearchForm(request.GET)
    
    # Если форма валидна, применяем фильтры
    if form.is_valid():
        # Получаем очищенные данные из формы
        query = form.cleaned_data.get('query')  # Поисковый запрос
        author = form.cleaned_data.get('author')  # Выбранный автор
        year_from = form.cleaned_data.get('year_from')  # Начало диапазона лет
        year_to = form.cleaned_data.get('year_to')  # Конец диапазона лет
        available_only = form.cleaned_data.get('available_only')  # Только доступные
        
        # Поиск по тексту (название, автор, ISBN)
        if query:
            books = books.filter(
                Q(title__icontains=query) |  # Название содержит query (без учета регистра)
                Q(author__name__icontains=query) |  # Имя автора содержит query
                Q(isbn__icontains=query)  # ISBN содержит query
            )
        
        # Фильтр по конкретному автору
        if author:
            books = books.filter(author=author)
        
        # Фильтр по году (больше или равно)
        if year_from:
            books = books.filter(publication_year__gte=year_from)  # gte - greater than or equal
        
        # Фильтр по году (меньше или равно)
        if year_to:
            books = books.filter(publication_year__lte=year_to)  # lte - less than or equal
        
        # Фильтр только доступных книг
        if available_only:
            books = books.filter(is_available=True)
    
    # Контекст для шаблона
    context = {
        'books': books,  # Отфильтрованный список книг
        'form': form,  # Форма для отображения текущих параметров фильтрации
    }
    return render(request, 'books/book_list.html', context)


# Детальная информация о книге
def book_detail(request, pk):
    """
    Отображает подробную информацию о конкретной книге.
    pk - первичный ключ (ID) книги.
    """
    # Получаем книгу по ID или возвращаем 404
    book = get_object_or_404(Book.objects.select_related('author'), pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


# Добавление новой книги
def book_create(request):
    """
    Обрабатывает создание новой книги.
    GET: отображает пустую форму
    POST: сохраняет данные и перенаправляет на страницу книги
    """
    if request.method == 'POST':
        # Создаем форму с переданными данными и файлами
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем книгу в БД
            book = form.save()
            # Добавляем сообщение об успехе
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            # Перенаправляем на страницу созданной книги
            return redirect('books:book_detail', pk=book.pk)
    else:
        # GET запрос - создаем пустую форму
        form = BookForm()
    
    # Рендерим шаблон с формой
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Добавить книгу'})


# Редактирование книги
def book_update(request, pk):
    """
    Обрабатывает редактирование существующей книги.
    GET: отображает форму с текущими данными
    POST: обновляет данные и перенаправляет на страницу книги
    """
    # Получаем книгу для редактирования
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Создаем форму с данными POST и привязываем к существующей книге
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Сохраняем изменения
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена!')
            return redirect('books:book_detail', pk=book.pk)
    else:
        # GET запрос - заполняем форму данными из книги
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Редактировать книгу'})


# Удаление книги
def book_delete(request, pk):
    """
    Обрабатывает удаление книги.
    GET: отображает страницу подтверждения удаления
    POST: удаляет книгу и перенаправляет на список книг
    """
    # Получаем книгу для удаления
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Удаляем книгу
        book.delete()
        messages.success(request, f'Книга "{book.title}" удалена!')
        return redirect('books:book_list')
    
    # GET запрос - показываем страницу подтверждения
    return render(request, 'books/book_confirm_delete.html', {'book': book})


# Список авторов
def author_list(request):
    """
    Отображает список всех авторов.
    """
    authors = Author.objects.all()  # Получаем всех авторов
    return render(request, 'books/author_list.html', {'authors': authors})


# Добавление автора
def author_create(request):
    """
    Обрабатывает создание нового автора.
    GET: отображает пустую форму
    POST: сохраняет автора и перенаправляет на список авторов
    """
    if request.method == 'POST':
        # Создаем форму с данными POST
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Сохраняем автора
            author = form.save()
            messages.success(request, f'Автор {author.name} успешно добавлен!')
            return redirect('books:author_list')
    else:
        # GET запрос - создаем пустую форму
        form = AuthorForm()
    
    return render(request, 'books/author_form.html', {'form': form})