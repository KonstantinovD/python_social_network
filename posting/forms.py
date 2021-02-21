from django import forms
from markdownx.fields import MarkdownxFormField
from markdownx.models import MarkdownxField

from posting.models import BlogPost


class PostForm(forms.ModelForm):
    # Все, что нужно для создания формы из модели, – указать, какую модель использовать в опциях класса Meta.
    # Django найдет нужную модель и автоматически построит форму.
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'tags')


class SearchContentForm(forms.Form):
    query = forms.CharField()


class SearchTagForm(forms.Form):
    query = forms.CharField()

# class PostForm(forms.ModelForm):
#     # Поле name имеет тип CharField. Этот тип полей будет отображаться как элемент <inputtype="text">
#     title = forms.CharField(max_length=50)
#
#     body = MarkdownxFormField()

    # # поля EmailField имеют валидацию и могут получать только корректные адреса
    # email = forms.EmailField()
    # to = forms.EmailField()
    #
    # # Каждый тип по умолчанию имеет виджет для отображения в HTML. Виджет может быть изменен с помощью параметра widget.
    # # В поле comments мы используем виджет Textarea
    # # для отображения HTML-элемента <textarea> вместо стандартного <input>
    # comments = forms.CharField(required=False, widget=forms.Textarea)