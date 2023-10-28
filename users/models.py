import jwt

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, middle_name, password):
        if email is None:
            raise TypeError("Пользователь обязательно должен иметь email")
        user = self.model(
            name=name,
            surname=surname,
            middle_name=middle_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, surname, middle_name, password):
        if password is None:
            raise TypeError(
                "Суперпользователь обязательно должен иметь пароль"
            )
        user = self.create_user(
            name=name,
            surname=surname,
            middle_name=middle_name,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("почта", db_index=True, unique=True)
    name = models.CharField("имя", max_length=255)
    surname = models.CharField("фамилия", max_length=255)
    middle_name = models.CharField("отчество", max_length=255)
    # 0 - обычный пользователь, 1 - HR, 2 - админ школы, 3 - админ сервиса
    role = models.IntegerField(
        "роль",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    """
    !!! ИЗМЕНИТЬ НА FK !!!!
    """
    organization = models.IntegerField("организация", blank=True, null=True)
    department = models.IntegerField("отдел", blank=True, null=True)
    position = models.IntegerField("должность", blank=True, null=True)
    """
    !!! ИЗМЕНИТЬ НА FK !!!!
    """
    last_login = models.DateTimeField("последний вход", auto_now_add=True)

    is_active = models.BooleanField("активен", default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField("создан", auto_now_add=True)
    updated_at = models.DateTimeField("обновлен", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "middle_name"]
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name + self.surname + self.middle_name

    def get_short_name(self):
        return self.name + self.surname

    def _generate_jwt_token(self):
        token = jwt.encode(
            {"id": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token
