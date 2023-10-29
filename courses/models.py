from django.db import models

from users.models import Department, Position, User, Organization


class Course(models.Model):
    name = models.CharField("название", max_length=150)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="организация"
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

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return f"Курс #{self.pk} - {self.name}"


class Material(models.Model):
    name = models.CharField("название", max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
    )
    file_link = models.CharField("ссылка на файл", max_length=255)

    class Meta:
        verbose_name = "материал"
        verbose_name_plural = "материалы"

    def __str__(self):
        return f"Материал #{self.pk} с курса {self.course.name}"


class Test(models.Model):
    name = models.CharField("название", max_length=150)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
    )

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"

    def __str__(self):
        return f"Тест #{self.pk} - {self.name}"


class Question(models.Model):
    text = models.TextField("вопрос")
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name="тест",
    )

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"

    def __str__(self):
        return f"Вопрос #{self.pk}"


class Answer(models.Model):
    text = models.TextField("вариант ответа")
    correct = models.BooleanField("является правильным", default=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="вопрос",
    )

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"

    def __str__(self):
        return f"Вариант ответа на вопрос {self.question.text}"


class Result(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name="тест"
    )
    correct_answers_count = models.IntegerField(
        "кол-во правильных ответов"
    )
    finish_date = models.DateTimeField(
        "дата сдачи",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"

    def __str__(self):
        return (
            f"Результат пользователя {self.user.name} в тесте {self.test.pk}"
        )
