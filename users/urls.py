from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from users.apps import UsersConfig
from users.views import RegistrationAPIView, ResetPasswordAPIView, UpdatePasswordAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "register/",
        RegistrationAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path('password-reset/', ResetPasswordAPIView.as_view(), name='password-reset'),
    path('password-reset/confirm/', UpdatePasswordAPIView.as_view(), name='password-reset-confirm'),
]
