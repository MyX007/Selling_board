import string
import random
from datetime import timedelta

from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordConfirm, ResetPasswordValidateToken, ResetPasswordRequestToken
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.core.mail import send_mail

from config import settings
from users.models import User
from users.serializers import UserSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer

from config.settings import EMAIL_HOST_USER


class RegistrationAPIView(CreateAPIView):
    """Регистрация пользователя."""
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data.get("password"))
        user.save()


class ResetPasswordAPIView(ResetPasswordRequestToken):
    """Запрос сброса пароля."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            email = request.data['email']
            try:
                token = ResetPasswordToken.objects.filter(user__email=email).latest('created_at')
                self.send_reset_email(email, token.key)
            except ResetPasswordToken.DoesNotExist:
                pass

        return response

    def send_reset_email(self, email, token):
        send_mail(
            subject="Восттановление пароля",
            message=f"users/password-reset/{token}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )


class UpdatePasswordAPIView(ResetPasswordConfirm):
    """Подтверждени сброса пароля"""
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["new_password"]
        token = serializer.validated_data["token"]
        uid = serializer.validated_data["uid"]

        user = get_object_or_404(User, pk=uid)
        if user:
            try:
                reset_password_token = ResetPasswordToken.objects.get(key=token)
            except ResetPasswordToken.DoesNotExist:
                return Response({"error": "Неверный токен!"}, status=status.HTTP_400_BAD_REQUEST)

            token_expiry_time = reset_password_token.created_at + timedelta(
                hours=getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)
            )

            if timezone.now() > token_expiry_time:
                reset_password_token.delete()  # Удаляем просроченный токен
                return Response(
                    {'error': 'Token has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            updated_user = reset_password_token.user

        updated_user.set_password(password)
        updated_user.save()

        return Response({"status": "OK"}, status=status.HTTP_200_OK)