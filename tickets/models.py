from django.db import models

from users.models import User


class Ticket(models.Model):
    text = models.TextField("текст обращения")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="отправитель",
    )

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        return f"Обращение #{self.pk}"


class TicketAnswer(models.Model):
    text = models.TextField("ответ на обращение")
    ticket = models.OneToOneField(
        Ticket,
        related_name="answer",
        on_delete=models.CASCADE,
        verbose_name="обращение",
    )

    class Meta:
        verbose_name = "ответ на обращение"
        verbose_name_plural = "ответы на обращения"

    def __str__(self):
        return f"Ответ #{self.pk}"
