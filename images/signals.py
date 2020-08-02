from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
# Мы регистрируем функцию users_like_changed как функцию-подписчик с помощью декоратора receiver
# и подписываемся на сигнал m2m_changed, отправляемый связями Image.users_like.through. Использование декоратора – один
# из способов добавления функции-подписчика. Кроме этого, можно использовать метод connect() объекта Signal.
# ...
# Сигналы Django выполняются синхронно и блокируются, поэтому не нужно обращаться к ним в асинхронных задачах. При этом
# возможность запускать такие задачи из сигналов остается доступной.
# ...
# Теперь мы должны связать сигнал и функцию-обработчик, которая будет вызываться каждый раз при срабатывании сигнала.
# Рекомендуемый способ зарегистрировать сигналы – импортировать их в методе ready() конфигурационного класса приложения.
# Django предоставляет реестр приложений, с помощью которого мы можем настраивать и управлять ими.
