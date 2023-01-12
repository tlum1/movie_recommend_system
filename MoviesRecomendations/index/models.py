from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Movie(models.Model):
    """
    Описание модели фильма
    Поля:
    1. Название фильма
    2. Рейтинг (высчитывается как средний рейтинг среди пользоветелей
    3. Описание
    4. Каст
    5. Постер
    6. Дополнительная информация
    7. Теги фильма
    8. ID
    """
    name = models.CharField(max_length=255, verbose_name="Title")
    genres = models.TextField(verbose_name="Genre")
    rating = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Rating")
    description = models.TextField(verbose_name="Description")
    director = models.TextField(verbose_name="Director", null=True)
    cast = models.TextField(verbose_name="Cast")
    poster_link = models.TextField(verbose_name="Poster link", default="")
    additional = models.TextField(verbose_name="additional")
    tags = models.TextField(verbose_name="Tags")
    movie_id = models.CharField(max_length=255, verbose_name="Movie ID")
    year = models.PositiveIntegerField(verbose_name="Year")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/movie/{self.pk}/'


class Rating(models.Model):
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", verbose_name="Movie", on_delete=models.CASCADE, related_name="Movie")
    user_rating = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="User rating")

    def __str__(self):
        return f"Movie: {self.movie}, rating: {self.user_rating}, user: {self.user}"
