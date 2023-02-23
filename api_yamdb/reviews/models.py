from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год выпуска')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        'Category',
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='titles',
        verbose_name='Категория',
        primary_key=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name
