from django.db import models
from django.urls import reverse

class Author(models.Model):
    """
    Модель для хранения информации об авторах книг.
    """
    # Поле для имени автора (строка до 100 символов)
    name = models.CharField(
        max_length=100, 
        verbose_name="Имя автора"  # Человекочитаемое название поля
    )
    
    # Поле для года рождения (целое число)
    birth_year = models.IntegerField(
        verbose_name="Год рождения",
        null=True,  # Разрешает NULL в базе данных
        blank=True  # Разрешает пустое значение в формах
    )
    
    # Поле для страны автора
    country = models.CharField(
        max_length=50, 
        verbose_name="Страна", 
        blank=True  # Может быть пустым
    )
    
    def __str__(self):
        """
        Строковое представление объекта.
        Используется в админке и при выводе в шаблонах.
        """
        return self.name
    
    class Meta:
        # Метаданные модели для админки и сортировки
        verbose_name = "Автор"  # Название в единственном числе
        verbose_name_plural = "Авторы"  # Название во множественном числе


class Book(models.Model):
    """
    Модель для хранения информации о книгах.
    Связана с моделью Author через внешний ключ.
    """
    # Название книги
    title = models.CharField(
        max_length=200, 
        verbose_name="Название книги"
    )
    
    # Связь с автором (внешний ключ)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='books',  # Обратная связь: author.books.all()
        verbose_name="Автор"
    )
    
    # Год публикации
    publication_year = models.IntegerField(
        verbose_name="Год публикации"
    )
    
    # ISBN (международный стандартный книжный номер)
    isbn = models.CharField(
        max_length=13,  # Стандартная длина ISBN-13
        verbose_name="ISBN", 
        unique=True  # Должен быть уникальным для каждой книги
    )
    
    # Количество страниц
    pages = models.IntegerField(
        verbose_name="Количество страниц"
    )
    
    # Описание книги (текстовое поле)
    description = models.TextField(
        verbose_name="Описание", 
        blank=True  # Может быть пустым
    )
    
    # Статус доступности книги
    is_available = models.BooleanField(
        default=True,  # По умолчанию книга доступна
        verbose_name="Доступна"
    )
    
    # Изображение обложки
    cover_image = models.ImageField(
        upload_to='book_covers/',  # Папка для загрузки файлов
        verbose_name="Обложка книги", 
        blank=True, 
        null=True  # Может быть NULL в базе данных
    )
    
    # Дата добавления записи (автоматически устанавливается при создании)
    created_at = models.DateTimeField(
        auto_now_add=True,  # Устанавливается только при создании
        verbose_name="Дата добавления"
    )
    
    def __str__(self):
        """
        Строковое представление книги.
        Формат: "Название - Имя автора"
        """
        return f"{self.title} - {self.author.name}"
    
    def get_absolute_url(self):
        """
        Возвращает URL для просмотра деталей книги.
        Используется в шаблонах для создания ссылок.
        """
        return reverse('book_detail', args=[str(self.id)])
    
    class Meta:
        # Метаданные модели
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']  # Сортировка по умолчанию: новые сначала