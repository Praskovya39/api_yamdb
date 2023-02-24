from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from django.conf import settings


class Title(models.Model):
    name = models.CharField(max_length=256,
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
        null=True,
        related_name='titles',
        verbose_name='Жанр')
    category = models.OneToOneField(
        'Category',
        on_delete=models.SET_NULL,
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


class Review(models.Model):
    title = models.ForeignKey('Title',
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Отзыв по произведению',
                              help_text='Укажите произведение')
    text = models.TextField(max_length=1000,
                            verbose_name='Отзыв',
                            help_text='Напишите Отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва')
    score = models.IntegerField(verbose_name='Оценка произведения',
                                help_text='Укажите рейтинг',
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(10)))
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    help_text='Укажите дату',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:settings.LEN_OUTPUT]


class Comment(models.Model):
    review = models.ForeignKey('Review',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий к отзыву')
    text = models.TextField(max_length=1000,
                            verbose_name='Комментарий',
                            help_text='Укажите комментарий')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.LEN_OUTPUT]