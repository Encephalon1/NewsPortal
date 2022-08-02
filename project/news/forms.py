from django import forms
from .models import Post, Category


class NewsForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'category',
            # Временная мера,чтобы при проверке кода не выдавало бы ошибку из-за значения NULL переменной.
            # Исправить на автоматическое подставление авторизованного автора.
            'post_author'
        ]


class ArticleForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'category',
            'post_author'
        ]
