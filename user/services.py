from __future__ import annotations

import os
from random import randrange
from typing import TYPE_CHECKING

import transliterate
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

if TYPE_CHECKING:
    from user.models import CustomUser
    from main.models import Castle


def forbidden_for_registered(method):
    def wrapper(self, request):
        if request.user.is_authenticated and not request.user.is_superuser and request.user.is_registered:
            return redirect("home")
        result = method(self, request)
        return result

    return wrapper


def generated_code() -> int:
    """Генерирует код для отправки на e-mail"""
    return randrange(1000, 9999)


def auto_slug(text) -> str:
    """Функция автоматически делает слаг каждому пользователю"""
    if not isinstance(text, str) or not text:
        text = f"{randrange(100000)}_anonim"
    return transliterate.slugify(text, language_code='ru')


class MixinSecondRegister:
    """ 2 Класс регистрации для обновления пустых полей race и nickname"""
    template_name: str = None
    class_form = None
    model_user: CustomUser = None
    model_castle: Castle = None

    @forbidden_for_registered
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {'form': self.class_form})

    @forbidden_for_registered
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        form = self.class_form(request.POST)
        if form.is_valid():
            self.create_castle_and_nickname(request, form)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': self.class_form})

    def create_castle_and_nickname(self, request: HttpRequest, form) -> CustomUser:
        """Метод для создания замка пользователя и входа пользователя в систему"""
        user = self.model_user.objects.get(pk=request.user.id)
        castle = self.model_castle.objects.create(name=form.data.get("castle_name"))
        user.nickname, user.race_id = form.data.get('nickname'), form.data.get('race')[-1]
        user.castle_id, user.is_registered = castle.id, True
        user.save()


class MixinAuthorizationEmail:
    """Класс для подтверждения почты пользователя"""
    template_name: str = None
    form_class = None

    @forbidden_for_registered
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {"form": self.form_class})

    @forbidden_for_registered
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        form = self.form_class(request.POST)
        if form.is_valid():
            session = request.session.get('code')
            if form.cleaned_data.get('code') == str(session.get('code')):
                del session['code']
                return redirect('register2')
            else:
                messages.error(request, "your cod don't correct")
                return redirect('authorization_code')

        else:
            messages.error(request, 'error repeat enter code')
            return redirect('authorization_code')


class MixinRegister:
    """Класс для первичной регистрации пользователя"""
    form_class = None
    template_name: str = None

    @forbidden_for_registered
    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    @forbidden_for_registered
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """Создаёт код в сессии отправляемый на почту для подтверждения e-mail"""
        form = self.form_class(request.POST)
        if form.is_valid():
            user: CustomUser = form.save()
            login(request, user)
            session = request.session['code'] = {}
            session['code'] = generated_code()
            try:
                send_mail(
                    subject='Код подтверждения электронной почты для игры ...',
                    message=str(session['code']),
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    recipient_list=[form.cleaned_data.get('email')],
                    fail_silently=False
                )

                messages.success(request, message='Письмо отправлено')
                return redirect('authorization_code')

            except Exception as ex:
                print(ex)
                logout(request)
                user.delete()
                messages.error(request, message='error register')
                return redirect('register')
        else:
            messages.error(request, message='error')
            return redirect('register')
