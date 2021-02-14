from django.urls import path
from . import views


urlpatterns = [
    path('blog/<int:pk>/', views.post, name='post_detail'),
    path('blog/', views.blog_posts, name='blog'),
    path('blog/newpost',
         views.create_post, name='create_post'),
]