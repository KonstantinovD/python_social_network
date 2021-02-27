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
]