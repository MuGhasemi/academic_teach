from django.urls import path, re_path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.LessonsListView.as_view(), name='home'),
    re_path(r'lesson/(?P<slug>[-\w]+)/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('add-lesson', views.LessonCreateView.as_view(), name='add_lesson'),
    path('student/lessons/', views.StudentLessonsView.as_view(), name='student_lesson'),
]
