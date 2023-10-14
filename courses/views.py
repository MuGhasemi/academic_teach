from django.shortcuts import render
from django.views.generic import ListView
from .models import Lesson
from .forms import SearchBoxForm
from django.db.models import Q
from accounts.models import User
from django.db.models import Count


def generate_user_info():
    user_info = {}
    user = User.objects.aggregate(
                        student_counts=Count('student'),
                        teacher_counts=Count('teacher'))

    user_info['student'] = user['student_counts']
    user_info['teacher'] = user['teacher_counts']
    return user_info

class LessonsListView(ListView):
    template_name = 'courses/home.html'
    model = Lesson
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = SearchBoxForm()
        context['count'] = generate_user_info()
        context['slider_contents'] = self.model.objects.order_by('date_created').all()[:5]
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