from django.urls import path
from . import views


urlpatterns = [
    path('blog/<int:pk>/', views.post, name='post_detail'),
    path('blog/<int:pk>/comment', views.post, name='post_detail'),
    path('blog/like', views.comment_like, name='comment_like'),
    path('blog/favorite', views.article_favorite, name='article_favorite'),
    path('blog/', views.blog_posts, name='blog'),
    path('blog/newpost',
         views.create_post, name='create_post'),
    path('blog/delete_post', views.delete_post, name='delete_post'),
    path('blog/update_post', views.update_post, name='update_post'),
    path('blog/reject_post', views.reject_post, name='reject_post'),
    path('blog/publish_post', views.publish_post, name='publish_post'),
    path('blog/not_published_blog_posts', views.not_published_blog_posts,
         name='not_published_blog_posts'),
    path('blog/draft_blog_posts', views.draft_blog_posts,
         name='draft_blog_posts'),
    path('blog/all_posts', views.all_posts,
         name='all_posts'),

]