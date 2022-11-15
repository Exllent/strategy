from django.http import (
    HttpResponseForbidden,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ForbiddenAdminPageMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseForbidden | HttpResponse:
        if request.path == "/admin/" and not request.user.is_superuser:
            return HttpResponseForbidden(request)
        response = self.get_response(request)
        return response


class CheckAuthenticateUserMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
        if not request.user.is_authenticated and request.path not in [
            reverse_lazy("register"),
            reverse_lazy("login"),
        ]:
            return redirect("register")
        response = self.get_response(request)
        return response
