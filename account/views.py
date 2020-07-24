from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


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
    # обработчик обернут в декоратор login_required. Он проверяет, авторизован ли пользователь. Если пользователь
    # авторизован, Django выполняет обработку. В противном случае пользователь перенаправляется на страницу
    # логина. При этом в GET-параметре задается next -адрес запрашиваемой страницы. Таким образом, после успешного
    # прохождения авторизации пользователь будет перенаправлен на страницу, куда он пытался попасть. Именно для этих
    # целей мы вставили скрытое поле next в форму логина.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


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
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        # в этом обработчике используем две формы: UserEditForm (для базовых сведений о пользователе)
        # и ProfileEditForm (для дополнительной, расширенной информации). Валидируем данные методом is_valid()
        # каждой из форм. Если обе формы заполнены корректно, сохраняем их с помощью метода save().
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
