from django import template
from posting.models import BlogPost

register = template.Library()


@register.inclusion_tag('posting/posts/latest_posts.html')
def show_latest_posts(count=3):  # Чтобы задать другое количество статей, используйте {% show_latest_posts 3 %}
    latest_posts = BlogPost.objects.all().order_by("-created_date")[:count]
    return {'latest_posts': latest_posts}  # функция тега возвращает словарь переменных вместо простого значения
