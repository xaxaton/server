from django.db import models
from django.core.validators import MinValueValidator


class Tariff(models.Model):
    name = models.CharField("название", max_length=150, unique=True)
    price = models.IntegerField(
        "цена", default=0, validators=[MinValueValidator(0)]
    )
    users_count = models.PositiveIntegerField("кол-во пользователей")
    tests_count = models.PositiveIntegerField("кол-во тестов")
    is_published = models.BooleanField("опубликован", default=True)

    class Meta:
        verbose_name = "тариф"
        verbose_name_plural = "тарифы"

    def __str__(self):
        return f"Тариф #{self.pk} - {self.name}"
