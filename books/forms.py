from django import forms
from .models import Book, Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'country']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя автора'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год рождения'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'pages', 'description', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название книги'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год публикации'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество страниц'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание книги'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BookSearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        label='Название', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по названию или автору...'})
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
           label='Автор', 
        empty_label="Все авторы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year_from = forms.IntegerField(
        required=False,
           label='Год с', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год с'})
    )
    year_to = forms.IntegerField(
        required=False,
           label='Год по', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год по'})
    )
    available_only = forms.BooleanField(
        required=False,
           label='Только доступные', 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )