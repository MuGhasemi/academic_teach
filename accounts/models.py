import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import AbstractUser, PermissionsMixin

class Student(models.Model):
    student_id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid1)
    username = models.CharField(
            max_length=150,
            unique=True,
            validators=[UnicodeUsernameValidator()],
            error_messages={"unique": ("A student with that username already exists."),})
    first_name = models.CharField(
            max_length=150,
            blank=True,
            null=True)
    last_name = models.CharField(
            max_length=150,
            blank=True,
            null=True)
    email = models.EmailField(
            max_length=200,
            unique=True,
            error_messages={"unique": ("A student with that email already exists."),})
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True,)
    is_delete = models.BooleanField(default=False,)
    date_joined = models.DateTimeField(default=timezone.now)
    student_image = models.ImageField(
            upload_to = 'student_image/',
            verbose_name="image",
            null = True,
            blank = True)

    class Meta:
        db_table = 'student'

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)