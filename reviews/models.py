from django.db import models


class Review(models.Model):
    text = models.TextField("текст отзыва")
    video = models.CharField(
        "ссылка на видео", max_length=255, null=True, blank=True
    )
    image = models.CharField(
        "ссылка на фото", max_length=255, null=True, blank=True
    )
    is_published = models.BooleanField("опубликовано", default=True)
    data = models.DateTimeField("дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"Отзыв #{self.pk}"
