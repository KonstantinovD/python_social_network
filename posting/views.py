from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import *
from .models import BlogPost, Tag
from .utils import create_tag_if_not_exist, get_posts_paginated, apply_post_filter


def blog_posts(request):
    """Display all blog posts"""

    # posts = BlogPost.objects.all().order_by('-created_date')
    posts = apply_post_filter(request)
    posts, page = get_posts_paginated(request, posts)

    all_tags = Tag.objects.all().order_by('name')

    post_form = PostForm()

    search_content_form = SearchContentForm()
    search_tag_form = SearchTagForm()

    return render(request, 'posting/blog.html',
                  {'posts': posts, 'post_form': post_form,
                   'search_content_form': search_content_form,
                   'search_tag_form': search_tag_form,
                   'page': page,
                   'all_tags': all_tags
                   })


def post(request, pk):
    """Display specific blog posts"""

    post_detail = get_object_or_404(BlogPost, pk=pk)

    return render(request, 'posting/post.html', {'post_detail': post_detail})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Publisher').exists(), )
def create_post(request):
    if request.method == 'POST':
        # request.method = 'GET'
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            new_item = post_form.save(commit=False)
            new_item.author = request.user
            create_tag_if_not_exist(cd['tags'])
            new_item.save()
    return HttpResponseRedirect(request.path.replace('/newpost', ''))
    # return redirect(request, 'blog/post/detail.html', new_comment=new_comment, comment_form=comment_form)
    # post_detail(request, year, month, day, post, new_comment=new_comment, comment_form=comment_form)

