from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)
    middle_name = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "surname",
            "middle_name",
            "password",
            "token",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    surname = serializers.CharField(max_length=255, read_only=True)
    middle_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Ошибка: Вы не указали почту.")

        if password is None:
            raise serializers.ValidationError("Ошибка: Вы не указали пароль.")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Пользователь с такой почтой и паролем не найден."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Похоже, ваш аккаунт удален или заблокирован. "
                "Обратитесь в тех. поддержку."
            )

        return {
            "email": user.email,
            "token": user.token,
        }
