import os
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from config.settings import LOGIN_REDIRECT_URL
from .models import Lesson, Enrollment
from .forms import SearchBoxForm, LessonForm
from django.db.models import Q
from accounts.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def generate_info(request):
    user = User.objects.aggregate(
                        student_counts=Count('student'),
                        teacher_counts=Count('teacher'))
    lesson = Lesson.objects.filter(is_active=True).count()
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
    queryset = Lesson.objects.filter(is_active=True)
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_contents'] = self.queryset.order_by('-date_created').all()[:5]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains = search) |
                Q(teacher__user__username__icontains = search)
            )
        return queryset

class LessonDetailView(DetailView):
    queryset = Lesson.objects.filter(is_active=True)
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

@method_decorator(login_required, name='dispatch')
class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_create.html'
    success_url = reverse_lazy('courses:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # TODO - sweetify.toast(request, 'You do not have permission to access this page.', 'error')
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # TODO - sweetify.toast(self.request, 'Book add failed.', 'error')
        return response


@method_decorator(login_required, name='dispatch')
class StudentLessonsView(ListView):
    template_name = 'courses/student_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        queryset = Enrollment.objects.filter(student=self.request.user.student)
        return queryset


@method_decorator(login_required, name='dispatch')
class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # TODO - sweetify.toast(request, 'You do not have permission to access this page.', 'error')
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        lesson = Lesson.objects.get(id=form.instance.id)
        old_photo_name = None
        if lesson.lesson_image.name:
            old_photo_path = lesson.lesson_image.path
            old_photo_name = (lesson.lesson_image.name).split('/')[1]
        new_book_image = self.request.FILES.get('lesson_image')
        if new_book_image and new_book_image.name != old_photo_name:
            lesson.lesson_image = new_book_image
            if old_photo_name:
                os.remove(old_photo_path)
        else:
            form.cleaned_data['lesson_image'] = None
        # TODO - sweetify.toast(self.request, 'Book edit successfully.', 'success')
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # TODO - sweetify.toast(self.request, 'Book edit failed.', 'error')
        return response
