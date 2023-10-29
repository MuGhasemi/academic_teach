from django.contrib import admin
from .models import User, Student, Teacher

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username",)}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (("Important dates"), {"fields": ("is_active", "date_joined",  "last_login", "user_type")}),
    )

    list_display = ("username", "email", "user_type", "is_active")

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
