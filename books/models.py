from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    birth_year = models.IntegerField(verbose_name="Год рождения", null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name="Страна", blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Автор")
    publication_year = models.IntegerField(verbose_name="Год публикации")
    isbn = models.CharField(max_length=13, verbose_name="ISBN", unique=True)
    pages = models.IntegerField(verbose_name="Количество страниц")
    description = models.TextField(verbose_name="Описание", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Доступна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']