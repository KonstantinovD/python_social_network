from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from common.constants import UserGroupNames

from actions.models import Action
from common.decorators import ajax_required
from posting.models import BlogPost
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.contrib import messages
from actions.utils import create_action
from django.db.models import Q
from django.contrib.admin.options import get_content_type_for_model


def user_login(request):
    # Система аутентификации определяет следующие модели:
    # 1) User – модель пользователя с основными полями username, password, email, first_name, last_name и is_active;
    # 2) Group – модель группы пользователей;
    # 3) Permission – разрешение для пользователя или группы пользователей на выполнение определенных действий.
    # Система также включает обработчики и формы
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # данные введены верно - сверяем их с данными в базе, юзая функцию authenticate(). Она принимает аргументы
            # request, username и password и возвращает объект пользователя User, если он успешно аутентифицирован
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                # если пользователь активный, авторизуем его на сайте. Это происходит посредством вызова
                # функции login(), которая запоминает пользователя в сессии
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
# в большинстве случаев достаточно использовать стандартные средства, уже реализованные в Django. Для работы
# с аутентификацией Django предоставляет обработчики-классы. Все они описаны в django.contrib.auth.views:
# +... LoginView – обработчик входа пользователя в его аккаунт;
# +... LogoutView – обработчик выхода пользователя из-под его учетной записи.
# В Django реализованы обработчики смены пароля пользователем:
# +... PasswordChangeView – обрабатывает форму смены пароля;
# +... PasswordChangeDoneView – обработчик, на который будет перенаправлен пользователь после успешной смены пароля.
# Также реализованы обработчики для восстановления пароля пользователя:
# +... PasswordResetView – обработчик восстановления пароля. Он генерирует временную ссылку с токеном и отправляет
#      ее на электронную почту пользователя;
# +... PasswordResetDoneView – отображает страницу с сообщением о том, что ссылка восстановления пароля была
#      отправлена на электронную почту;
# +... PasswordResetConfirmView – позволяет пользователю указать новый пароль;
# +... PasswordResetCompleteView – отображает сообщение об успешной смене пароля.
# Вышеописанные обработчики экономят время, когда на сайте нужно реализовать функционал аутентификации. Все они
# используют классы форм и HTML-шаблоны по умолчанию, но при желании их можно переопределить и воспользоваться своими.


@login_required
def dashboard(request):
    # По умолчанию отображаем все действия.

    time_threshold = timezone.now() - timedelta(days=30)
    group_moderator = Group.objects.get(name=UserGroupNames.MODERATOR)
    actions = Action.objects.exclude(
        user=request.user).filter(
        Q(user__in=request.user.following.all())
        | Q(user__in=group_moderator.user_set.all(),
            target_ct=get_content_type_for_model(request.user),
            target_id=request.user.pk),
        created__gte=time_threshold)[:10]

    # content_type = get_content_type_for_model(request.user)
    # object_id = request.user.pk
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard', 'actions': actions})


# Хороший пример if-блоков для обработки формы
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Вместо сохранения пароля «как есть», мы используем метод set_password()
            # модели User. Он сохранит пароль в зашифрованном виде
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            group = Group.objects.get(name=UserGroupNames.BASE_USER)
            group.user_set.add(new_user)
            group.save()
            Profile.objects.create(user=new_user)
            # create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    user_profile = request.user.profile
    show_nickname_v_checked = 'checked' if user_profile.params['show_nickname'] == 'true' else ''
    show_name_v_checked = 'checked' if user_profile.params['show_name'] == 'true' else ''

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        # в этом обработчике используем две формы: UserEditForm (для базовых сведений о пользователе)
        # и ProfileEditForm (для дополнительной, расширенной информации). Валидируем данные методом is_valid()
        # каждой из форм. Если обе формы заполнены корректно, сохраняем их с помощью метода save().
        if user_form.is_valid() and profile_form.is_valid():
            if not ('show_real_name' in request.POST or 'show_nickname' in request.POST):
                messages.error(request,
                               'Режим ображения имени/никнейма настроен неверно: выберите хотя бы одно значение')
            else:
                if 'show_real_name' in request.POST:
                    show_name = 'true'
                else:
                    show_name = 'false'
                if 'show_nickname' in request.POST:
                    show_nickname = 'true'
                else:
                    show_nickname = 'false'

                user_form.save()

                new_profile = profile_form.save(commit=False)
                new_profile.params['show_name'] = show_name
                new_profile.params['show_nickname'] = show_nickname
                new_profile.save()

                messages.success(request, 'Profile updated successfully')
                return render(request, 'account/dashboard.html', {'section': 'dashboard'})
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form,
                   'show_nickname_v': show_nickname_v_checked, 'show_name_v': show_name_v_checked})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    # TODO: change 'draft' to 'published'
    posts = user.created_posts.order_by('-created_date')[:3]
    # .filter(status='draft')
    favorites = BlogPost.objects.filter(id__in=user.profile.favorites).order_by('-created_date')[:3]

    if request.method == 'POST':
        group_publisher = Group.objects.get(name=UserGroupNames.PUBLISHER)
        if 'group_publisher' in request.POST:
            group_publisher.user_set.add(user)
            group_publisher.save()
        else:
            group_publisher.user_set.remove(user)
            group_publisher.save()

        group_publisher_with_grant = Group.objects.get(name=UserGroupNames.PUBLISHER_WITH_GRANT)
        if 'group_publisher_with_grant' in request.POST:
            group_publisher_with_grant.user_set.add(user)
            group_publisher_with_grant.save()
        else:
            group_publisher_with_grant.user_set.remove(user)
            group_publisher_with_grant.save()

        group_moderator = Group.objects.get(name=UserGroupNames.MODERATOR)
        if 'group_moderator' in request.POST:
            group_moderator.user_set.add(user)
            group_moderator.save()
        else:
            group_moderator.user_set.remove(user)
            group_moderator.save()

        create_action(request.user, 'change_groups', user)

    return render(request, 'account/user/detail.html',
                  {'section': 'people', 'user': user, 'posts': posts,
                   'favorites':  favorites})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)

                backrelcontact = Contact.objects.filter(user_from=user, user_to=request.user).first()
                if backrelcontact is not None:
                    create_action(request.user, 'is_following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})
# Обработчик user_follow очень похож на image_like, который мы создали ранее. Так как мы используем промежуточную модель
# для связи пользователя и его подписчиков, стандартные методы add() и remove() менеджера недоступны. Поэтому мы
# напрямую создаем и удаляем, используя модель Contact.
