from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from main.models import Castle
from user.forms import UserFirstRegisterForm, UserLoginForm, UserSecondRegisterForm, AuthorizationEmailForm
from user.models import CustomUser
from user.services import MixinSecondRegister, MixinRegister, MixinAuthorizationEmail
from user.services import forbidden_for_registered


def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('register')


class UserLogin(FormView):
    """Класс для авторизации пользователя на сайт"""
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    @forbidden_for_registered
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    @forbidden_for_registered
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: UserLoginForm) -> HttpResponseRedirect:
        user: CustomUser = form.get_user()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form: UserLoginForm) -> HttpResponseRedirect:
        messages.error(self.request, message='Не верно введён логин или пароль')
        return redirect('login')


class Register(View, MixinRegister):
    """класс для первичной регистрации пользователя"""
    form_class = UserFirstRegisterForm
    template_name = 'user/register.html'


class SecondRegister(MixinSecondRegister, View):
    """Класс для вторичной регистрации пользователя"""
    template_name = 'user/register2.html'
    class_form = UserSecondRegisterForm
    model_user = CustomUser
    model_castle = Castle


class AuthorizationEmail(View, MixinAuthorizationEmail):
    """Класс для подтверждение e-mail пользователя"""
    template_name = 'user/authorization.html'
    form_class = AuthorizationEmailForm
