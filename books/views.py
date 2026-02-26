# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Book, Author
from .forms import BookForm, AuthorForm, BookSearchForm

# Главная страница - вывод информации
def home(request):
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    available_books = Book.objects.filter(is_available=True).count()
    recent_books = Book.objects.all()[:5]
    
    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'available_books': available_books,
        'recent_books': recent_books,
    }
    return render(request, 'books/home.html', context)

# Список книг с фильтрацией и поиском
def book_list(request):
    books = Book.objects.select_related('author').all()
    form = BookSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        author = form.cleaned_data.get('author')
        year_from = form.cleaned_data.get('year_from')
        year_to = form.cleaned_data.get('year_to')
        available_only = form.cleaned_data.get('available_only')
        
        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) |
                Q(isbn__icontains=query)
            )
        
        if author:
            books = books.filter(author=author)
        
        if year_from:
            books = books.filter(publication_year__gte=year_from)
        
        if year_to:
            books = books.filter(publication_year__lte=year_to)
        
        if available_only:
            books = books.filter(is_available=True)
    
    context = {
        'books': books,
        'form': form,
    }
    return render(request, 'books/book_list.html', context)

# Детальная информация о книге
def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author'), pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

# Добавление новой книги
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Добавить книгу'})

# Редактирование книги
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена!')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Редактировать книгу'})

# Удаление книги
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Книга "{book.title}" удалена!')
        return redirect('books:book_list')
    
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# Список авторов
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/author_list.html', {'authors': authors})

# Добавление автора
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Автор {author.name} успешно добавлен!')
            return redirect('books:author_list')
    else:
        form = AuthorForm()
    
    return render(request, 'books/author_form.html', {'form': form})