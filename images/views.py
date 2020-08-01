from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена.
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            # Добавляем пользователя к созданному объекту.
            new_item.save()
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})
# Этот обработчик выполняет следующие действия:
# - получает начальные данные и создает объект формы. Эти данные содержат url и title картинки со стороннего сайта, они
# будут переданы в качестве аргументов GET-запроса JavaScript-инструментом, который мы добавим чуть позже.
# - если форма отправлена POST-запросом, проверяет ее корректность. Если данные валидны, создает новый объект Image,
# но пока не сохраняет его в базу данных, передавая аргумент commit=False;
# - привязывает текущего пользователя к картинке. Так мы узнаем, кто загрузил это изображение;
# - сохраняет объект image в базу данных;
# - наконец, создает уведомление и перенаправляет пользователя на канонический URL новой картинки. Мы пока
# не реализовали метод get_absolute_url() для модели Image, но добавим его чуть позже.


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images','image': image})