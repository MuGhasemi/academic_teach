from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Lesson
from .forms import SearchBoxForm
from django.db.models import Q
from accounts.models import User
from django.db.models import Count


def generate_info(request):
    user = User.objects.aggregate(
                        student_counts=Count('student'),
                        teacher_counts=Count('teacher'))
    lesson = Lesson.objects.all().count()
    context = {
        'student': user['student_counts'],
        'teacher': user['teacher_counts'],
        'lesson': lesson
    }
    return render(request, 'partials/header_content.html', context)


def search_box(request):
    context = {
        'search': SearchBoxForm()
    }
    return render(request, 'partials/search.html', context)


class LessonsListView(ListView):
    template_name = 'courses/home.html'
    model = Lesson
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_contents'] = self.model.objects.order_by('-date_created').all()[:5]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains = search) |
                Q(teacher__user__username__icontains = search)
            )
            if queryset.count() == 0:
                print('Not Found!')
        return queryset

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset