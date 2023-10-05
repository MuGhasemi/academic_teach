import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES =(
        ('admin','Admin'),
        ('student','Student'),
        ('teacher','Teacher'),

    )
    email = models.EmailField(
        max_length=200,
        unique=True)
    is_delete = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=7,
        choices=USER_TYPE_CHOICES,
        default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def is_student(self):
        return self.user_type == 'student'

    def is_teacher(self):
        return self.user_type == 'teacher'

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student')
    student_image = models.ImageField(
            upload_to = 'student_image/',
            verbose_name="image",
            null = True,
            blank = True)

    class Meta:
        db_table = 'student'

    def __str__(self) -> str:
        return self.user.username

class Teacher(models.Model):
    teacher_id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid1)
    username = models.CharField(
            max_length=150,
            unique=True,
            validators=[UnicodeUsernameValidator()],
            error_messages={"unique": ("A teacher with that username already exists."),})
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
            error_messages={"unique": ("A teacher with that email already exists."),})
    description = models.TextField(
            blank=True,
            null=True)
    field = models.CharField(
            max_length=100,
            blank=True,
            null=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True,)
    is_delete = models.BooleanField(default=False,)
    date_joined = models.DateTimeField(default=timezone.now)
    teacher_image = models.ImageField(
            upload_to = 'teacher_image/',
            verbose_name="image",
            null = True,
            blank = True)

    class Meta:
        db_table = 'teacher'

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
