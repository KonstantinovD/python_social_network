from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # пример своего логин-обработчика
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    # Шаблоны для доступа к обработчикам смены пароля.
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('redirect/', redirect_view)
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),  # Убедитесь, что этот шаблон будет находиться перед
    # шаблоном user_detail. В противном случае запрос по адресу /users/follow/ подойдет к регулярному отображению
    # шаблона user_detail, при этом будет вызван не тот обработчик, который мы ожидаем. Помните, что Django проверяет
    # каждый URL-шаблон по порядку, пока не найдет первый подходящий.
    path('users/<username>/', views.user_detail, name='user_detail'),
]
# Вы можете закомментировать то, что мы указывали в файле urls.py для приложения account, и вместо этого
# подключить пути приложения django.contrib.auth.urls:    path('', include('django.contrib.auth.urls')),
# p. s. у меня подобное не отрабатывало
