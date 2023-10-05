from django.db import models
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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher')
    student_image = models.ImageField(
            upload_to = 'teacher_image/',
            verbose_name="image",
            null = True,
            blank = True)

    class Meta:
        db_table = 'teacher'

    def __str__(self) -> str:
        return self.user.username