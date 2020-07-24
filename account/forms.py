from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Django предоставляет класс UserCreationForm, который расположен в модуле
# django.contrib.auth.forms. Он очень похож на класс формы, созданный нами.
class UserRegistrationForm(forms.ModelForm):
    # мы добавили два поля: password и password2 – для задания и подтверждения пароля.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        # set <email> field required
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    # Мы создали модельную форму для пользователя, включив в нее только поля username, first_name и email.
    # Они будут валидироваться в соответствии с типом полей модели. Например, если пользователь введет логин, который
    # уже используется, ему вернется сообщение с указанием на ошибку, из-за того что в модели поле username
    # определено как unique=True.
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # В методе clean_password2() мы проверяем, совпадают ли оба пароля. Если они отличаются, то будет возвращена ошибка.
    # Мы можем добавлять методы с названием вида clean_<fieldname>() для любого поля формы, чтобы Django проверял
    # соответствующее поле и в случае некорректных данных привязывал ошибку к нему.
    # Кроме того, у форм реализован метод clean(), который проверяет корректность всей формы. Он применяется,
    # когда необходимо выполнить проверку взаимосвязанных полей.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


# UserEditForm – позволит пользователям менять имя, фамилию, e-mail (поля встроенной в Django модели)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# ProfileEditForm – позволит модифицировать доп сведения, которые мы сохраняем в модели Profile (дату рождения и аватар)
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
