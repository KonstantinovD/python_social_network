from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Profile(models.Model):
    # Поле «один к одному» user позволит нам связать дополнительные данные с конкретным пользователем.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    # Поле photo имеет тип ImageField. Для работы с ним нам необходимо установить библиотеку изображений Pillow
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

# Кроме использования ссылки типа «один к одному», Django позволяет полностью заменить модель пользователя. Для этого
# наш класс должен быть наследником AbstractUser, который реализует базовые методы для пользователя.
# Более подробно: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#substituting-a-custom-user-model.
# Использование собственной модели пользователя сделает наш код более гибким, но может стать причиной чуть
# более сложной интеграции со сторонними приложениями, которые взаимодействуют с моделью пользователя Django


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

        def __str__(self):
            return '{} follows {}'.format(self.user_from, self.user_to)

# Этот фрагмент описывает модель Contact, которая будет использоваться для связи пользователей. Она содержит
# следующие поля:
# - user_from – ForeignKey на пользователя-подписчика;
# - user_to – ForeignKey на пользователя, на которого подписались;
# - created – поле DateTimeField с auto_now_add=True для сохранения времени создания связи.
# В базе данных индекс автоматически создается для полей ForeignKey. Мы также создадим индекс по полю created с помощью
# атрибута db_index=True. Это поможет ускорить запросы с фильтрацией и сортировкой по нему.


# Динамическое добавление поля following в модель User
User.add_to_class('following', models.ManyToManyField(
    'self', through=Contact,
    related_name='followers',
    # Отношение определено с параметром symmetrical=False. Когда мы создаем поле ManyToManyField на ту же самую модель,
    # Django воспроизводит симметричные отношения. Поэтому мы явно указали symmetrical=False, чтобы оно было
    # несимметричным. Так, если вы подпишетесь на меня, я не буду автоматически добавлен в список ваших подписчиков
    symmetrical=False))
# Если модель User определена в нашем приложении, мы можем добавить в нее это поле напрямую. Но в нашем случае это
# невозможно, т. к. используется модель пользователя из django.contrib.auth. Поэтому мы добавим поле динамически.
# Здесь мы обращаемся к методу модели add_to_class(), чтобы с легкостью изменить ее. такой способ добавления атрибута
# рекомендуется использовать только в особенных случаях
# !!!
# Когда вы используете промежуточную модель для отношений «многие ко многим», некоторые методы менеджеров перестают
# работать, например add(), create(), remove(). Теперь вам будет нужно явно добавлять или удалять объекты
# промежуточной модели.
