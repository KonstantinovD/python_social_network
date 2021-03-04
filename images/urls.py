from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('analyse_image', views.analyse_image, name='analyse_image'),
]


