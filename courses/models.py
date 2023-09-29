from django.db import models
from accounts.models import Student, Teacher
from django.utils import timezone

class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        db_index = True,)
    description = models.TextField()
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name='lessons',)
    start_date = models.DateField(default=timezone.now)
    capacity = models.PositiveSmallIntegerField(default=20,)
    number_of_sessions = models.PositiveSmallIntegerField(default=10,)
    days_of_week = models.PositiveSmallIntegerField(default=3,)
    lesson_image = models.ImageField(
        upload_to='lesson_image/',
        blank=True,
        null = True,)
    is_active = models.BooleanField(
        default=True,)
    is_delete = models.BooleanField(
        default=False,)

    class Meta():
        db_table = 'lesson'
        ordering = ['start_date']

    def __str__(self):
        return self.title
