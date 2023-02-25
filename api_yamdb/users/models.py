from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
STAFF = 'moderator'
ADMIN = 'admin'

CHOISES = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор')
    )


class User(AbstractUser):
    email = models.EmailField(max_length=50,unique=True, blank=False)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    bio = models.TextField(max_length=500)
    role = models.CharField(max_length=15,choices=CHOISES, default='user')
    confirmation_code = models.CharField(max_length=15)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Проверка пользователя на администратора."""
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка пользователя на модератора."""
        return self.role == 'moderator'

    @property
    def is_user(self):
        """Проверка пользователя на юзера."""
        return self.role == 'user'

    #class Meta:
    #    """Сортировка и проверка на уникальность """
    #
    #  constraints = [
    #        models.UniqueConstraint(
    #            fields=['username', 'email'],
    #            name='unique_username_email'
    #        )
    #    ]