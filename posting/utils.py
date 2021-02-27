from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector


from posting.models import Tag
from .forms import SearchContentForm, SearchTagForm
from .models import BlogPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.constants import *


def create_tag_if_not_exist(array_field):
    tag_folder = []
    for tag in array_field:
        if tag not in tag_folder:
            tag_folder.append(tag)
            Tag.objects.get_or_create(name=tag)


def apply_post_filter(request):
    if 'content' in request.GET:
        form = SearchContentForm()
        query = None
        if 'query' in request.GET:
            form = SearchContentForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result_posts = BlogPost.objects.annotate(
                search=SearchVector('title', 'body'), ).filter(search=query)

            add_post_ids_to_session(request, result_posts)

            return result_posts
    if 'tag' in request.GET:
        form = SearchTagForm()
        query = None
        if 'query' in request.GET:
            form = SearchTagForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result_posts = BlogPost.objects.filter(tags__icontains=query)

            add_post_ids_to_session(request, result_posts)

            return result_posts

    if 'reset' in request.GET:
        result_posts = BlogPost.objects.all().order_by('-created_date')

        add_post_ids_to_session(request, result_posts)

        return result_posts

    if 'author_id' in request.GET:
        author_id = request.GET['author_id']
        user = User.objects.get(pk=author_id)
        result_posts = BlogPost.objects.filter(author = user).order_by('-created_date')
        add_post_ids_to_session(request, result_posts)
        return result_posts

    if 'post_ids' in request.GET:
        post_ids_str = request.GET['post_ids']
        post_ids_str = post_ids_str[1:-1]
        post_ids_array = post_ids_str.split(',')
        result_posts = BlogPost.objects.filter(id__in=post_ids_array).order_by('-created_date')

        add_post_ids_to_session(request, result_posts)

        return result_posts

    if 'tag_value' in request.GET:
        tag_value = request.GET['tag_value']
        result_posts = BlogPost.objects.filter(tags__icontains=tag_value)
        add_post_ids_to_session(request, result_posts)
        return result_posts

    post_ids = request.session.get('s_posts', None)
    if post_ids is None:
        result_posts = BlogPost.objects.all().order_by('-created_date')

        add_post_ids_to_session(request, result_posts)

        return result_posts
    else:
        result_posts = BlogPost.objects\
            .filter(id__in=post_ids).order_by('-created_date')
        return result_posts


def add_post_ids_to_session(request, result_posts):
    posts_l = list(answer.id for answer in result_posts)
    request.session['s_posts'] = posts_l


def get_posts_paginated(request, posts):
    # posts = request.session['s_posts']

    page = request.GET.get('page')
    if page is None:
        page = request.session.get('s_page', None)

    paginator = Paginator(posts, POST_COUNT_ON_PAGE)
    #
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
        page = 1
        # request.session['s_page'] = 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        page = paginator.num_pages
        # request.session['s_page'] = paginator.num_pages
    #
    return posts, page


