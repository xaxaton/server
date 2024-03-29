# Generated by Django 3.2.4 on 2023-10-29 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_auto_20231029_1647"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
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
                ("text", models.TextField(verbose_name="вариант ответа")),
                (
                    "correct",
                    models.BooleanField(
                        default=False, verbose_name="является правильным"
                    ),
                ),
            ],
            options={
                "verbose_name": "вариант ответа",
                "verbose_name_plural": "варианты ответа",
            },
        ),
        migrations.CreateModel(
            name="Course",
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
                    "name",
                    models.CharField(max_length=150, verbose_name="название"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.department",
                        verbose_name="отдел",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.organization",
                        verbose_name="организация",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.position",
                        verbose_name="должность",
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
        migrations.CreateModel(
            name="Question",
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
                ("text", models.TextField(verbose_name="вопрос")),
            ],
            options={
                "verbose_name": "вопрос",
                "verbose_name_plural": "вопросы",
            },
        ),
        migrations.CreateModel(
            name="Result",
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
                    "correct_answers_count",
                    models.IntegerField(
                        verbose_name="кол-во правильных ответов"
                    ),
                ),
                (
                    "finish_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата сдачи"
                    ),
                ),
            ],
            options={
                "verbose_name": "результат",
                "verbose_name_plural": "результаты",
            },
        ),
        migrations.CreateModel(
            name="Test",
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
                    "name",
                    models.CharField(max_length=150, verbose_name="название"),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.course",
                        verbose_name="курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "тест",
                "verbose_name_plural": "тесты",
            },
        ),
        migrations.DeleteModel(
            name="Tariff",
        ),
        migrations.AddField(
            model_name="result",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.test",
                verbose_name="тест",
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.test",
                verbose_name="тест",
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.question",
                verbose_name="вопрос",
            ),
        ),
    ]
