from django.db import models
from accounts.models import Student, Teacher
from django.utils import timezone
from django.utils.text import slugify

class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        db_index = True,)
    description = models.TextField()
    slug = models.SlugField(
        editable=False,
        unique=True,
        blank=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name='lessons',)
    date_created = models.DateField(auto_now_add=True,)
    registration_start = models.DateField(
        default = timezone.now() + timezone.timedelta(days=3),)
    registration_deadline = models.DateField(
        default = timezone.now() - timezone.timedelta(days=3),)
    start_date = models.DateField(default=timezone.now,)
    price = models.PositiveIntegerField(default=0)
    capacity = models.PositiveSmallIntegerField(default=20,)
    number_of_sessions = models.PositiveSmallIntegerField(default=10,)
    days_of_week = models.PositiveSmallIntegerField(default=3,)
    lesson_image = models.ImageField(
        upload_to='lesson_image/',
        blank=True,
        null=True,)
    is_active = models.BooleanField(
        default=True,)
    is_delete = models.BooleanField(
        default=False,)

    class Meta():
        db_table = 'lesson'
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments')
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='enrollments')
    registration_date = models.DateTimeField(auto_now_add=True,)

    class Meta():
        db_table = 'enrollment'
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} - {self.lesson}"