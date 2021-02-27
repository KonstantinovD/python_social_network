from django import template
from posting.models import BlogPost
from django.contrib.auth.models import Group

register = template.Library()


@register.inclusion_tag('posting/posts/latest_posts.html')
def show_latest_posts(count=3):  # Чтобы задать другое количество статей, используйте {% show_latest_posts 3 %}
    latest_posts = BlogPost.objects.all().order_by("-created_date")[:count]
    return {'latest_posts': latest_posts}  # функция тега возвращает словарь переменных вместо простого значения


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False


@register.filter(name='get_comment_likes')
def get_comment_likes(comment):
    val = 0
    for preference in comment.comment_likes.all():
        if preference.value > 0:
            val = val + 1
    return val


@register.filter(name='get_comment_dislikes')
def get_comment_dislikes(comment):
    val = 0
    for preference in comment.comment_likes.all():
        if preference.value < 0:
            val = val + 1
    return val


@register.filter(takes_context=True, name='get_user_preference')
def get_user_preference(comment, user):
    comment_like = comment.comment_likes.filter(user=user).first()
    if comment_like is None:
        return 0
    return comment_like.value


@register.filter(name='get_user_full_name')
def get_user_full_name(user):
    user_profile = user.profile

    show_nickname = user_profile.params['show_nickname'] == 'true'
    show_name = user_profile.params['show_name'] == 'true'

    if show_nickname and show_name:
        return user.get_full_name() + ' (' + user.username + ')'
    if show_nickname:
        return user.username
    if show_name:
        return user.get_full_name()

    return ''


@register.filter(name='reword_user_action')
def reword_user_action(action):
    # if action.target == user:
    if action.verb == 'is_following':
        return "подписался на Вас"
    if action.verb == 'creates_article':
        return "опубликовал статью"
    return action.verb