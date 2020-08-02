import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action


def create_action(user, verb, target=None):
    # Поиск похожего действия, совершенного за последнюю минуту.
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    if not similar_actions:
        # Недавнее Action не найдено, создаем новое.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
# create_action() позволяет создать Action и связать ее с некоторым объектом target, если он будет передан в качестве
# аргумента. Мы будем использовать данную функцию для большего удобства при создании записи об активности пользователя
