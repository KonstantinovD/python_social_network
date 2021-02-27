from datetime import datetime

from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
from django.contrib.postgres.fields import ArrayField
import json

# Create your models here.


class DateCreateModMixin(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(blank=True, null=True)


class BlogPost(DateCreateModMixin):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted')
    )

    title = models.CharField(max_length=50)

    body = MarkdownxField()

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='created_posts', default=None)

    slug = models.SlugField(max_length=250, unique_for_date='created_date')

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='draft')

    tags = ArrayField(models.CharField(max_length=20, blank=True), size=8, default=[])

    published_date = models.DateTimeField(blank=True, null=True)

    def formatted_markdown(self):
        return markdownify(self.body)

    def body_summary(self):
        return markdownify(self.body[:300] + "...")

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # Атрибут related_name позволяет получить доступ к комментариям конкретной статьи. Теперь мы сможем обращаться
    # к статье из комментария, используя запись comment.post, и к комментариям статьи при помощи post.comments.all().
    # Если бы мы не определили related_name, юзалось бы имя связанной модели с постфиксом _set (например, comment_set).
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments', default=None)

    body = models.TextField()

    num_related_to_article = models.IntegerField(blank=True, default=0)
    index_referenced_to_related_to_article = models.IntegerField(blank=True, default=None, null=True)
    index_referenced_to = models.IntegerField(blank=True, default=None, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # добавили булевое поле active, чтобы можно было скрывать комментарии

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:  # поле created для сортировки комментариев в хронологическом порядке.
        ordering = ('created',)

    def __str__(self):
        return self.body


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                             related_name='comment_likes', default=None)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.comment) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "comment", "value")
