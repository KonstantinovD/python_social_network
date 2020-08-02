from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    # user – указывает пользователя, который добавляет изображение в закладки. Это поле является внешним ключом и
    # использует связь «один ко многим».
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()  # сылка на оригинальное изображение
    image = models.ImageField(upload_to='images/%Y/%m/%d/')  # файл изображения;
    description = models.TextField(blank=True)  # необязательное (blank=True) поле описания
    # <created> – дата и время создания объекта в базе данных.
    # - Аргумент db_index=True говорит Django о необходимости создать индекс по этому полю. Индексы баз данных улучшают
    # производительность. Рассмотрите возможность добавления db_index=True для полей, которые часто используются в
    # filter(), exclude(), order_by().
    # - Для полей с unique=True и ForeignKey индексы создаются автоматически.
    # - Для определения составного индекса можно использовать Meta.index_together
    created = models.DateField(auto_now_add=True, db_index=True)
    # Когда мы определяем поле ManyToManyField, Django создает промежуточную таблицу, содержащую первичные ключи
    # объектов связанных моделей. Этот тип поля предоставляет менеджер отношения «многие ко многим», с помощью которого
    # можно обращаться к связанным объектам в виде     - image.users_like.all()
    # или из объекта пользователя user как             - user.images_likes.all().
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    # Мы переопределим метод save() модели Image
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
    # use method save from parent class Image - но т к это название самой модели (Image), то мы сохраняем свой же класс
        super(Image, self).save(*args, **kwargs)
        # функция slugify() автоматически формирует его из переданного заголовка, после чего мы сохраняем объект
        # картинки. Таким образом, слаг будет генерироваться автоматически, юзеру не нужно будет вводить его вручную

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
