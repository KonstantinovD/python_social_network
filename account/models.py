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
