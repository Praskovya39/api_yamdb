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
    role = models.CharField(max_length=15,choices=CHOISES)
    confirmation_code = models.CharField(max_length=15)

    def __str__(self):
        return self.username
    