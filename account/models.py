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
