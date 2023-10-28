# Generated by Django 3.2.4 on 2023-10-27 19:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        max_length=254,
                        unique=True,
                        verbose_name="почта",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="имя")),
                (
                    "surname",
                    models.CharField(max_length=255, verbose_name="фамилия"),
                ),
                (
                    "middle_name",
                    models.CharField(max_length=255, verbose_name="отчество"),
                ),
                (
                    "role",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(3),
                        ],
                        verbose_name="роль",
                    ),
                ),
                (
                    "organization",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="организация"
                    ),
                ),
                (
                    "department",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="отдел"
                    ),
                ),
                (
                    "position",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="должность"
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="последний вход"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="активен"),
                ),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="создан"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="обновлен"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
