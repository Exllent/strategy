from django.urls import path

from user.views import Register, SecondRegister, UserLogin, user_logout, AuthorizationEmail

urlpatterns: list[path] = [
    path(route='register/', view=Register.as_view(), name='register'),
    path(route='register2/', view=SecondRegister.as_view(), name='register2'),
    path(route='login/', view=UserLogin.as_view(), name='login'),
    path(route='logout/', view=user_logout, name='logout'),
    path(route="authorization_code/", view=AuthorizationEmail.as_view(), name="authorization_code"),
]
