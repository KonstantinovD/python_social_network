import base64
import os
import time
import uuid

import numpy as np
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookmarks.settings import MEDIA_ROOT
from .forms import ImageCreateForm, ImageDTOForm
from .models import Image, ImageDTO, AnalyzedData
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from django.conf import settings
import cv2
import json

@login_required
def analyse_image(request):
    image_form = None
    image = None
    img_instance = None
    pk = None
    string = None
    if request.method == 'GET':
        if 'image_loaded' in request.GET:
            img_url = request.session['image_url']
            img_data = request.session['color_data']


            multiple_models_data = []

            for value in img_data.values():
                analysed_data = AnalyzedData()
                analysed_data.model = value[0]
                analysed_data.r = value[1]
                analysed_data.g = value[2]
                analysed_data.b = value[3]
                multiple_models_data.append(analysed_data)


            return render(request, 'neural/analyse_image.html',
                          {'img': img_url, 'img_data': multiple_models_data})
        else:
            image_form = ImageDTOForm()

    if request.method == 'POST':
        if 'image_id' in request.GET:
            image_id = request.GET['image_id']
            image_dto = ImageDTO.objects.get(pk=image_id)

            img = cv2.imread(image_dto.image.path)
            # encode image as jpeg
            _, img_encoded = cv2.imencode('.jpg', img)
            # send http request with image and receive response
            response = requests.post('http://127.0.0.1:5000/image',
                                     data=img_encoded.tostring())
            json_var = json.loads(response.text)

            base64_bytes = json_var['imageBytes'].encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)

            # npdecoded = base64.decodebytes(json_var['imageBytes']).encode('ascii')
            nparr = np.fromstring(message_bytes, np.uint8)

            res_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            id = uuid.uuid1()
            res_img_url = MEDIA_ROOT[:-1] + '\\analyse\\' + str(id.int) + '.jpg'

            cv2.imwrite(res_img_url, res_img)

            request.session['image_url'] = '/media/analyse/' + str(id.int) + '.jpg'
            request.session['color_data'] = json_var['analyzed_data']

            return render(request, 'neural/analyse_image.html',
                          {'wait': True, 'image': image_dto})


        else:
            img_saved = ImageDTOForm(instance=img_instance, data=request.POST, files=request.FILES)
            image = img_saved.save()
            pk = image.pk

    return render(request, 'neural/analyse_image.html',
                  {'image_form': image_form, 'image': image,
                   'pk': pk})



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
            # create_action(request.user, 'bookmarked image', new_item)
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
                # create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
            # возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})
# В этом обработчике мы формируем QuerySet для получения всех изображений, сохраненных в закладки. Затем создаем объект
# Paginator и получаем постраничный список картинок. Если желаемой страницы не существует, обрабатываем исключение
# EmptyPage. В случае AJAX-запроса возвращаем пустое значение, чтобы остановить дальнейшую прокрутку списка картинок.
# Передаем контекст в два HTML-шаблона:
# - для AJAX-запросов используем list_ajax.html. Он содержит только HTML для показа картинок;
# - для стандартных запросов используем list.html. Этот шаблон наследуется от base.html и показывает полноценную
# страницу, на которую добавлен список картинок из list_ajax.html.



