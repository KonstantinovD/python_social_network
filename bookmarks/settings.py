"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nq7-vuc2d6uxfl1&rbafg^n+ces_ib$jk&)6x%k%4*p%kpy3o%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bookmarksite.com',
                 'localhost',
                 '127.0.0.1',
                 '4bd3c7c83c3d.ngrok.io'
                 ]


# Application definition

INSTALLED_APPS = [
    # Позже мы добавим шаблоны для страниц аутентификации. Django ищет шаблоны в порядке приложений в INSTALLED_APPS,
    # поэтому, размещая наше приложение первым, мы гарантируем, что именно его шаблоны будут использоваться
    # по умолчанию вместо шаблонов, объявленных в других приложениях
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'images.apps.ImagesConfig',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    # В настройке MIDDLEWARE задаются два промежуточных слоя:
    # +... AuthenticationMiddleware – связывает пользователей и запросы с помощью сессий;
    # +... SessionMiddleware – обрабатывает сессию запроса.
    # Промежуточный слой – это класс с методами, которые выполняются при обработке каждого запроса и формировании
    # ответа. Мы будем использовать их еще несколько раз на протяжении этой книги и даже создадим
    # собственный промежуточный слой в главе 13.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'account/../templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookmarks',
        'USER': 'postgres',
        'PASSWORD': 'katukov',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# указывает адрес, куда Django будет перенаправлять юзера при успешной авторизации, если не указан GET-параметр next;
LOGIN_REDIRECT_URL = 'dashboard'
# адрес, куда нужно перенаправлять юзера для входа в систему, например из обработчиков с декоратором login_required
LOGIN_URL = 'login'
# адрес, перейдя по которому, пользователь выйдет из своего аккаунта
LOGOUT_URL = 'logout'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# проперти для того, чтобы Django знал, где хранить медиафайлы, загруженные пользователями
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Own authentication
# Django будет использовать бэкэнды по порядку, поэтому теперь пользователь сможет аутентифицироваться и с помощью
# электронной почты. Идентификационные данные сначала будут проверены ModelBackend. Если этот бэкэнд не вернет
# объект пользователя, Django попробует аутентифицировать его с помощью нашего класса, EmailAuthBackend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend'
]

SOCIAL_AUTH_FACEBOOK_KEY = '984489861973468'  # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b748482710f779325a1a0b02f12cb61f'  # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}
# Django динамически добавляет метод get_absolute_url() для каждой модели, перечисленной в настройке
# ABSOLUTE_URL_OVERRIDES. В этом случае из настройки будет возвращаться соответствующий модели URL. В примере для
# пользователя мы возвращаем URL по имени user_detail. Теперь мы можем вызвать метод get_absolute_url() для объекта
# User, чтобы получить его канонический адрес
