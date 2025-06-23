from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = "__all__"


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор сброса пароля"""
    class Meta:
        model = User
        fields = ['email']


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """Сериализатор подтверждения сброса пароля"""
    new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)

