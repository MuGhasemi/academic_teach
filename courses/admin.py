from django.contrib import admin
from .models import Lesson, Enrollment

class LessonAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title",)}),
        (("info"), {"fields": (
                                        "teacher",
                                        "description",
                                        "price",
                                        "capacity",
                                        "number_of_sessions",
                                        "days_of_week",
                                        "lesson_image")}),
        (("Important dates"), {"fields": (
                                        "registration_start",
                                        "registration_deadline",
                                        "start_date",
                                        "is_active",
                                        "is_delete",)}),
    )

    list_display = ("title", "teacher", "price", "is_active")

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "registration_date")


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
