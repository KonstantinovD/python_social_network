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


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


