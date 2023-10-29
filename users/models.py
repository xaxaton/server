import jwt

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from courses.models import Tariff


class Organization(models.Model):
    name = models.CharField("название", max_length=250, unique=True)
    description = models.TextField("описание", blank=True, null=True)
    logo = models.CharField("логотип", max_length=255)
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name="тариф",
    )

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"

    def __str__(self):
        return f"Организация '{self.name}'"


class Department(models.Model):
    name = models.CharField("название", max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="организация",
    )

    class Meta:
        verbose_name = "отдел"
        verbose_name_plural = "отделы"

    def __str__(self):
        return f"Отдел '{self.name}'"


class Position(models.Model):
    name = models.CharField("название", max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="организация",
    )

    class Meta:
        verbose_name = "должность"
        verbose_name_plural = "должности"

    def __str__(self):
        return f"Должность '{self.name}'"


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
        user.is_active = False
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
        user.role = 3
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("почта", db_index=True, unique=True)
    name = models.CharField("имя", max_length=255)
    surname = models.CharField("фамилия", max_length=255)
    middle_name = models.CharField("отчество", max_length=255)
    role = models.IntegerField(
        "роль",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=(
            "0 - обычный пользователь, 1"
            " - HR, 2 - админ школы, 3 - админ сервиса"
        ),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="организация",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="отдел",
        blank=True,
        null=True,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name="должность",
        blank=True,
        null=True,
    )
    last_login = models.DateTimeField("последний вход", auto_now_add=True)

    is_active = models.BooleanField("активен", default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField("создан", auto_now_add=True)
    updated_at = models.DateTimeField("обновлен", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "middle_name"]
    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return f"{self.surname} {self.name}  {self.middle_name}"

    def get_short_name(self):
        return f"{self.name} {self.surname}"

    def _generate_jwt_token(self):
        token = jwt.encode(
            {"id": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def save(self, *args, **kwargs):
        if self.role >= 1:
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)
