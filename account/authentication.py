from django.contrib.auth.models import User


# Бэкэнд по умолчанию ModelBackend аутентифицирует пользователей, используя модель из django.contrib.auth. Это подходит
# для большинства проектов. Но можно создать свой бэкэнд для нового способа аутентификации (например, через LDAP или
# любую другую систему).  https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#other-authentication-sources
# Каждый раз, когда мы пытаемся аутентифицировать пользователя функцией authenticate(), Django пробует применить каждый
# из бэкэндов, указанных в AUTHENTICATION_BACKENDS, по очереди, пока не дойдет до того, который успешно аутентифицирует
# пользователя. Если ни один из бэкэндов не сможет этого сделать, пользователь не будет аутентифицирован в нашей системе
# Django предоставляет простой способ создания собственного бэкэнда аутентификации. Достаточно описать класс, в котором
# есть два метода:
# +... authenticate() – принимает в качестве параметров объект запроса request и идентификационные данные пользователя.
#      Он должен возвращать объект пользователя, если данные корректны; в противном случае – None.
#      Аргумент request имеет тип HttpRequest, но может быть и None;
# +... get_user()     – принимает ID и должен вернуть соответствующий объект пользователя.
# Создать свой бэкэнд – это значит создать Python-класс, который реализует эти два метода.
class EmailAuthBackend(object):
    """Выполняет аутентификацию пользователя по e-mail."""
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
