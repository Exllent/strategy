from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from race.constants import RaceChoices
from user.models import CustomUser


class AuthorizationEmailForm(forms.Form):
    code = forms.CharField(label="E-mail code", max_length=4, min_length=4)


class UserSecondRegisterForm(forms.Form):
    nickname = forms.CharField(
        label="Ник-нэйм", max_length=25, min_length=4, help_text="Введите свой ник-нейм"
    )
    castle_name = forms.CharField(
        label="Название замка",
        max_length=25,
        min_length=4,
        help_text="Введите название своего замка",
    )
    race = forms.CharField(
        label="Великая раса",
        widget=forms.Select(choices=RaceChoices.choices),
        help_text="Выберите расу за которую хотите играть, выбор единоразовый в будущем его нельзя будет изменить",
    )


class UserLoginForm(AuthenticationForm):
    pass


class UserFirstRegisterForm(UserCreationForm):
    login = forms.CharField(label="Логин", widget=forms.TextInput())
    email = forms.EmailField(
        label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Пароль", help_text="password", widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        help_text="Repeat password",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = CustomUser
        fields = [
            "login",
            "email",
            "password1",
            "password2",
        ]
