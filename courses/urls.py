from django.urls import path, re_path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.LessonsListView.as_view(), name='home'),
    re_path(r'lesson/(?P<slug>[-\w]+)/', views.LessonDetailView.as_view(), name='lesson_detail')
]
