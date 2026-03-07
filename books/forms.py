# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import Book, Author

# Форма для создания и редактирования авторов
class AuthorForm(forms.ModelForm):
    """
    Форма для работы с моделью Author.
    Позволяет создавать и редактировать записи об авторах.
    """
    class Meta:
        # Привязка к модели Author
        model = Author
        # Поля, которые будут отображаться в форме
        fields = ['name', 'birth_year', 'country']
        # Настройка внешнего вида полей (виджеты)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',  # CSS класс Bootstrap
                'placeholder': 'Имя автора'  # Подсказка в поле ввода
            }),
            'birth_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год рождения'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Страна'
            }),
        }

    """
    Форма для работы с моделью Author.
    Позволяет создавать и редактировать записи об авторах.
    """
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя автора'
            }),
            'birth_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год рождения'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Страна'
            }),
        }

# Форма для создания и редактирования книг
class BookForm(forms.ModelForm):
    """
    Форма для работы с моделью Book.
    Содержит все поля книги с настроенным отображением.
    """
    class Meta:
        # Привязка к модели Book
        model = Book
        # Все поля модели, которые будут в форме
        fields = ['title', 'author', 'publication_year', 'isbn', 'pages', 'description', 'is_available', 'cover_image']
        # Настройка виджетов для каждого поля
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'  # Выпадающий список авторов
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год публикации'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN'  # Международный стандартный книжный номер
            }),
            'pages': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество страниц'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,  # Высота текстового поля в 4 строки
                'placeholder': 'Описание книги'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'  # Стиль для чекбокса
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control'  # Поле для загрузки изображения
            }),
        }

# Форма для поиска книг (не связана с моделью)
class BookSearchForm(forms.Form):
    """
    Форма для фильтрации и поиска книг.
    Используется на странице каталога или поиска.
    """
    # Поиск по названию (текстовое поле)
    query = forms.CharField(
        required=False,  # Поле необязательное для заполнения
        label='Название',  # Метка поля в шаблоне
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или автору...'
        })
    )
    
    # Фильтр по автору (выпадающий список)
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),  # Все авторы из базы данных
        required=False,
        label='Автор',
        empty_label="Все авторы",  # Значение по умолчанию
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Фильтр по году (начало диапазона)
    year_from = forms.IntegerField(
        required=False,
        label='Год с',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год с'
        })
    )
    
    # Фильтр по году (конец диапазона)
    year_to = forms.IntegerField(
        required=False,
        label='Год по',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год по'
        })
    )
    
    # Фильтр только доступных книг (чекбокс)
    available_only = forms.BooleanField(
        required=False,
        label='Только доступные',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )