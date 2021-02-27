from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from .forms import *
from .models import BlogPost, Tag, Preference
from .postdetails.postgetails import fill_new_comment_data, process_post_request
from .utils import create_tag_if_not_exist, get_posts_paginated, apply_post_filter
from posting.templatetags.blog_tags import get_user_full_name


def blog_posts(request):
    """Display all blog posts"""

    # posts = BlogPost.objects.all().order_by('-created_date')
    posts = apply_post_filter(request)
    posts, page = get_posts_paginated(request, posts)

    all_tags = Tag.objects.all().order_by('name')

    search_content_form = SearchContentForm()
    search_tag_form = SearchTagForm()

    return render(request, 'posting/blog.html',
                  {'posts': posts,
                   'search_content_form': search_content_form,
                   'search_tag_form': search_tag_form,
                   'page': page,
                   'all_tags': all_tags
                   })


def post(request, pk):
    """Display specific blog posts"""

    post_detail = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        return process_post_request(request, post_detail)

    if request.method == 'GET':
        comment_form = CommentForm()
        comments = post_detail.comments.filter(active=True)

        name = get_user_full_name(post_detail.author)
        # first_name = post_detail.author.first_name
        # last_name = post_detail.author.last_name
        # if first_name is not None:
        #     name = name + first_name + ' '
        # if last_name is not None:
        #     name = name + last_name + ' '

        return render(request, 'posting/post.html',
                      {'post_detail': post_detail,
                       'comment_form': comment_form,
                       'comments': comments,
                       'user_name': name})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Publisher').exists(), )
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            new_item = post_form.save(commit=False)
            new_item.author = request.user
            create_tag_if_not_exist(cd['tags'])
            new_item.save()
            create_action(request.user, 'creates_article', new_item)
            return HttpResponseRedirect(request.path.replace('/newpost', '?reset=true'))
        else:
            return HttpResponseRedirect(request.path)
    if request.method == 'GET':
        post_form = PostForm()
        return render(request, 'posting/posts/create_article.html', {'post_form': post_form,})

    # return redirect(request, 'blog/post/detail.html', new_comment=new_comment, comment_form=comment_form)
    # post_detail(request, year, month, day, post, new_comment=new_comment, comment_form=comment_form)


# Используем два декоратора для функции. Декоратор <login_required> не даст неавторизованным пользователям
# доступ к этому обработчику. Декоратор <require_POST> возвращает ошибку HttpResponseNotAllowed
# В Django также реализованы декораторы <required_GET>, и <require_http_methods>, принимающий список разрешенных методов
# @ajax_required
# Теперь, если вы обратитесь к URL’у http://127.0.0.1:8000/images/like/ напрямую через браузер, то получите ошибку 400.
@login_required
@require_POST
def comment_like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    # user_id = request.POST.get('user_id')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            comment_like = comment.comment_likes.filter(user=request.user).first()

            # Если вы вызываете add() и передаете в него пользователя, который уже связан с текущей картинкой, дубликат
            # не будет создан. Аналогично при вызове remove() и попытке удалить пользователя, который не связан с
            # изображением, ошибки нет. Еще один полезный метод (many to many) – clear(). Он удаляет все отношения
            if action == 'like':
                if comment_like is not None:
                    if comment_like.value == 1:
                        comment_like.delete()
                        return JsonResponse({'status': 'ok',
                                             'action': action, 'method': 'delete'})
                    else:
                        comment_like.value = 1
                        comment_like.save()
                        return JsonResponse({'status': 'ok',
                                             'action': action, 'method': 'add'})
                else:
                    comment_like = Preference()
                    comment_like.user = request.user
                    comment_like.comment = comment
                    comment_like.value = 1
                    comment_like.save()
                    return JsonResponse({'status': 'ok',
                                         'action': action, 'method': 'add'})
            if action == 'dislike':
                if comment_like is not None:
                    if comment_like.value == -1:
                        comment_like.delete()
                        return JsonResponse({'status': 'ok',
                                             'action': action, 'method': 'delete'})
                    else:
                        comment_like.value = -1
                        comment_like.save()
                        return JsonResponse({'status': 'ok',
                                             'action': action, 'method': 'add'})
                else:
                    comment_like = Preference()
                    comment_like.user = request.user
                    comment_like.comment = comment
                    comment_like.value = -1
                    comment_like.save()
                    return JsonResponse({'status': 'ok',
                                         'action': action, 'method': 'add'})
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def article_favorite(request):
    post_id = int(request.POST.get('id'))
    if post_id in request.user.profile.favorites:
        profile = request.user.profile
        profile.favorites.remove(post_id)
        profile.save()
    else:
        profile = request.user.profile
        profile.favorites.append(post_id)
        profile.save()
    return JsonResponse({'status': 'ok'})


