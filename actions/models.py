from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions',
                             db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    # В обобщенных связях ContentType играет роль посредника между моделями. Для
    # создания такой связи нам необходимо добавить в модель три поля:
    # - ForeignKey на модель ContentType. Оно будет указывать на модель, с которой связана текущая;
    # - поле для хранения ID связанного объекта. Обычно определяется как PositiveIntegerField для идентификаторов,
    # автоматически созданных Django
    # - поле для определения связи и управления ей. Обращается к предыдущим двум полям, объект типа GenericForeignKey.
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
                                  related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    # Django не создает столбец на уровне базы данных для полей GenericForeignKey. Вместо этого сохраняются значения
    # полей target_ct и target_id. Оба определены параметрами blank=True и null=True, поэтому наличие связанного
    # объекта вовсе не обязательно при сохранении объекта Action.

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
# определяем модель Action для хранения информации о действиях пользователя. Она содержит следующие поля:
# - user – пользователь, который выполнил действие. Внешний ключ ForeignKey на стандартную модель Django – User;
# - verb – информация о том, какое действие было выполнено;
# - created – дата и время, показывающие, когда был создан объект. Мы используем auto_now_add=True, чтобы автоматически
# выставлять текущее время, когда объект сохраняется в базу данных.
# С помощью такой модели мы можем сохранять простые действия, такие как «пользователь X сделал что-то».
# ...
# Для того чтобы указывать объект, над которым было произведено действие (например, «пользователь X добавил в закладки
# картинку Y» или «пользователь X подписался на обновления пользователя Y»), необходимо добавить поле target. Однако,
# как мы уже знаем, ForeignKey может ссылаться только на одну модель, а в нашем случае нужна возможность указывать
# объект любой модели. Тут на помощь приходит !!! подсистема типов содержимого Django !!!
#                               |
#                               |
#                               |
#                               V
# В Django добавлено приложение, расположенное в django.contrib.contenttypes,
# которое знает про все модели установленных приложений нашего проекта
# и предоставляет обобщенный интерфейс для обращения к ним.
# Приложение django.contrib.contenttypes автоматически добавляется в список
# INSTALLED_APPS, если вы создаете проект командой startproject. Оно использует-
# ся другими приложениями из пакета contrib, например подсистемой аутенти-
# фикации и сайтом администрирования.
# В приложении contenttypes определена модель ContentType. Ее объекты содер-
# жат сведения о реальных моделях проекта и автоматически создаются при до-
# бавлении новых. ContentType содержит следующие поля:
# - app_label – имя приложения системы, к которому относится описывае-
# мая модель. Значение автоматически подставляется из атрибута app_label
# опций Meta модели. Например, модель Image принадлежит приложению images;
# - model – название класса модели;
# - name – понятное человеку название модели. Значение подставляется из
# атрибута verbose_name опций Meta модели.
# ...
# EXAMPLE:
# ...
# >>> from django.contrib.contenttypes.models import ContentType
# >>> image_type = ContentType.objects.get(app_label='images', model='image')
# >>> image_type
# <ContentType: image>
# ...
# Чтобы получить класс отслеживаемой модели, можно вызвать метод model_class()
# ...
# >>> image_type.model_class()
# <class 'images.models.Image'>
# ...
# Также часто необходимо получить объект ContentType для определенной мо-
# дели. Это можно сделать следующим образом:
# ...
# >>> from images.models import Image
# >>> ContentType.objects.get_for_model(Image)
# <ContentType: image>

