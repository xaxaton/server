from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import (
    User, Organization, Tariff,
    Department, Position
)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)
    middle_name = serializers.CharField(max_length=255)
    role = serializers.IntegerField(read_only=True)
    organization = serializers.DictField(allow_null=True, read_only=True)
    department = serializers.CharField(allow_null=True, read_only=True)
    position = serializers.CharField(allow_null=True, read_only=True)
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "surname",
            "middle_name",
            "organization",
            "role",
            "department",
            "position",
            "password",
        ]

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]):
            raise serializers.ValidationError("Ошибка: Почта занята.")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    surname = serializers.CharField(max_length=255, read_only=True)
    middle_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.IntegerField(read_only=True)
    organization = serializers.DictField(allow_null=True, read_only=True)
    department = serializers.CharField(allow_null=True, read_only=True)
    position = serializers.CharField(allow_null=True, read_only=True)
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
        response = {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "middle_name": user.middle_name,
            "role": user.role,
            "token": user.token,
        }
        if user.organization:
            response["organization"] = {
                "name": user.organization.name,
                "logo": user.organization.logo,
            }
        if user.department:
            response["department"] = user.department.name
        if user.position:
            response["position"] = (user.position.name,)
        return response


class TariffIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    logo = serializers.CharField()
    tariff = TariffIdSerializer()

    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        if Organization.objects.filter(name=validated_data["name"]):
            raise serializers.ValidationError(
                "Ошибка: Такая организация уже зарегистрирована."
            )
        current_tariff = Tariff.objects.get(id=validated_data["tariff"]["id"])
        validated_data["tariff"] = current_tariff
        return Organization.objects.create(**validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name"
        ]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name"
        ]


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(required=False)
    position = PositionSerializer(required=False)\

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "surname",
            "middle_name",
            "id",
            "department",
            "position",
        ]


class TariffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    price = serializers.IntegerField()
    users_count = serializers.IntegerField()
    tests_count = serializers.IntegerField()

    class Meta:
        model = Tariff
        fields = "__all__"
