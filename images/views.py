from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required


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
                  {'section': 'images', 'image': image})


# Используем два декоратора для функции. Декоратор <login_required> не даст неавторизованным пользователям
# доступ к этому обработчику. Декоратор <require_POST> возвращает ошибку HttpResponseNotAllowed
# В Django также реализованы декораторы <required_GET>, и <require_http_methods>, принимающий список разрешенных методов
@ajax_required
# Теперь, если вы обратитесь к URL’у http://127.0.0.1:8000/images/like/ напрямую через браузер, то получите ошибку 400.
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # Если вы вызываете add() и передаете в него пользователя, который уже связан с текущей картинкой, дубликат
            # не будет создан. Аналогично при вызове remove() и попытке удалить пользователя, который не связан с
            # изображением, ошибки нет. Еще один полезный метод (many to many) – clear(). Он удаляет все отношения
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})
