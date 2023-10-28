import sweetify
import os
from datetime import date
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
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
    lesson = Lesson.objects.filter(is_delete=False).count()
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
    queryset = Lesson.objects.filter(is_delete=False)
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
    queryset = Lesson.objects.filter(is_delete=False)
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        lesson = self.get_object()
        if self.request.user.user_type == 'student':
            std = self.request.user.student
            enrollment = Enrollment.objects.filter(student=std, lesson=lesson).first()
            context['enrollment'] = enrollment
        elif self.request.user.user_type == 'teacher':
            context['students_list'] = lesson.enrollments.values_list('student__user__first_name',
                                                                      'student__user__last_name',
                                                                      'student__user__email')
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
            sweetify.toast(request, 'شما اجازه دسترسی به این صفحه را ندارید!', 'error')
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        sweetify.toast(self.request, 'درس با موفقیت اضافه شد.', 'success')
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        sweetify.toast(self.request, 'درس اضافه نشد!', 'error')
        return response


@method_decorator(login_required, name='dispatch')
class UserLessonsView(ListView):
    template_name = 'courses/user_lesson_list.html'
    context_object_name = 'lists'

    def get_queryset(self):
        if self.request.user.user_type == 'student':
            queryset = Enrollment.objects.filter(student=self.request.user.student)
        elif self.request.user.user_type == 'teacher':
            queryset = Lesson.objects.filter(teacher = self.request.user.teacher)
        return queryset


@method_decorator(login_required, name='dispatch')
class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            sweetify.toast(request, 'شما اجازه دسترسی به این صفحه را ندارید!', 'error')
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
        sweetify.toast(self.request, 'ویرایش درس با موفقیت انجام شد.', 'success')
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        sweetify.toast(self.request, 'ویرایش درس ناموفق بود!', 'error')
        return response

@method_decorator(login_required, name='dispatch')
class StudentRegisterLesson(View):

    def post(self, request):
        if not request.user.user_type == 'student':
            sweetify.toast(self.request, 'شما دانشجو نیستید!', 'error', timer=5000)
            return redirect(LOGIN_REDIRECT_URL)
        std = request.user.student
        lesson = Lesson.objects.get(id=request.POST['lesson'])
        if lesson.capacity == 0:
            sweetify.toast(self.request, 'ظرفیت کلاس تکمیل است!', 'error', timer=5000)
            return redirect(LOGIN_REDIRECT_URL)
        if Enrollment.objects.filter(student=std, lesson=lesson).first() != None:
            sweetify.toast(self.request, 'شما قبلا ثبت نام کرده اید', 'success', timer=5000)
            return redirect(LOGIN_REDIRECT_URL)
        if std.credit < lesson.price:
            sweetify.toast(self.request, 'اعتبار شما کافی نیست!', 'error', timer=5000)
            return redirect('accounts:credit')
        Enrollment.objects.create(
                                student=std,
                                lesson=lesson
                                )
        sweetify.toast(self.request, 'ثبت نام شما انجام شد.', 'success', timer=5000)
        std.credit -= lesson.price
        std.save()
        return redirect('courses:student_lesson')


@login_required
def delete_lesson(request, slug):
    if not request.method == 'GET':
        return redirect(LOGIN_REDIRECT_URL)
    if not request.user.is_staff:
        sweetify.toast(request, 'شما اجازه دسترسی به این صفحه را ندارید!', 'error')
        return redirect(LOGIN_REDIRECT_URL)
    lesson = get_object_or_404(Lesson, slug=slug)
    enrollments = lesson.enrollments.all()
    enrollments.delete()

    lesson.is_active = False
    lesson.is_delete = True
    lesson.save()
    sweetify.toast(request, 'درس با موفقیت حذف شد.', 'success', timer=4000)
    return redirect(LOGIN_REDIRECT_URL)

