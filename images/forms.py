from urllib import request
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image, ImageDTO


class ImageCreateForm(forms.ModelForm):
    # используем ModelForm модели Image, которая включает поля title, url, description. Пользователи не будут вручную
    # заполнять адрес. Вместо этого мы добавим JavaScript-инструмент для выбора картинки на любом постороннем сайте,
    # а наша форма будет получать URL изображения в качестве параметра.
    # Мы заменили виджет по умолчанию для поля url и используем HiddenInput. Этот виджет формируется как input-элемент
    # с атрибутом type="hidden". Мы сделали это для того, чтобы пользователи не видели поле <url>.
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }

    # метод clean_url() для валидации поля url. Django дает возможность проверять каждое поле формы по отдельности
    # с помощью методов вида clean_<fieldname>()
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    # Этот метод принимает необязательный аргумент <commit>, который позволяет настроить поведение (действительно ли
    # нужно сохранять объект в базу данных). Если commit равен False, метод вернет объект модели, но не сохранит его.
    # Мы переопределим save() формы, чтобы скачивать файл картинки и сохранять его.
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)  # creates image but not saves it
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())
        # Скачиваем изображение по указанному адресу.
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
# Данная функция
# - создает объект image, вызвав метод save() с аргументом commit=False;
# - получает URL из атрибута cleaned_data формы;
# - генерирует название изображения, совмещая слаг и расширение картинки;
# - использует Python-пакет urllib, чтобы скачать файл картинки, и вызывает метод save() поля изображения, передавая
# в него объект скачанного файла, ContentFile. Используется commit=False, чтобы покане сохранять объект в базу данных;
# - при переопределении метода важно оставить стандартное поведение, поэтому сохраняем объект изображения в базу данных
# только в том случае, если commit равен True.


class ImageDTOForm(forms.ModelForm):
    class Meta:
        model = ImageDTO
        fields = ('image',)

