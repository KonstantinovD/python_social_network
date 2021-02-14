from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import BlogPost


def blog_posts(request):
    """Display all blog posts"""

    posts = BlogPost.objects.all().order_by('-created_date')
    post_form = PostForm()

    return render(request, 'posting/blog.html', {'posts': posts, 'post_form': post_form})


def post(request, pk):
    """Display specific blog posts"""

    post_detail = get_object_or_404(BlogPost, pk=pk)

    return render(request, 'posting/post.html', {'post_detail': post_detail})


# Если заменить <post> на <slug>, например, то получите
# create_comment() got an unexpected keyword argument 'post'
@login_required
def create_post(request):
    post_form = PostForm()

    # new_post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
    #                          publish__month=month, publish__day=day)
    # comment_form = CommentForm()
    # new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        # request.method = 'GET'
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            post_form.save()
    return HttpResponseRedirect(request.path.replace('/newpost', ''))
    # return redirect(request, 'blog/post/detail.html', new_comment=new_comment, comment_form=comment_form)
    # post_detail(request, year, month, day, post, new_comment=new_comment, comment_form=comment_form)

