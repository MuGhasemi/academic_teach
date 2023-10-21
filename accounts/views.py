import os
from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginUserForm, RegisterUserForm, EditUserForm, EditStudentForm
from .models import User, Student
from django.contrib.auth import authenticate, login, logout
from config.settings import LOGIN_URL, LOGIN_REDIRECT_URL, SIGN_UP_URL
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginUserForm

    def get(self, request):
        if request.user.is_authenticated:
            # TODO - create message for you are login
            return redirect(LOGIN_REDIRECT_URL)
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['email'],
                                password=cd['password'])
            if user is not None:
                login(request, user)
                # TODO - create message for login successfully
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(LOGIN_REDIRECT_URL)
            # TODO - create message for login failed
        # TODO - create message for login failed
        return redirect(LOGIN_URL)



class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = RegisterUserForm

    def get(self, request):
        if request.user.is_authenticated:
            # TODO - create message for you are login
            return redirect(LOGIN_REDIRECT_URL)
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if  cd['password'] == cd['confirm_password']:
                user = User.objects.create(
                    username = cd['username'],
                    first_name = cd['first_name'],
                    last_name  = cd['last_name'],
                    email = cd['email'],
                    user_type = 'student'
                    )
                user.set_password(cd['confirm_password'])
                user.save()
                Student.objects.create(user=user, student_image=None)
                # TODO - create message for register successfully
                return redirect(LOGIN_URL)
            # TODO - create message for password does not match
            return redirect(SIGN_UP_URL)
        # TODO - create message for register failed
        return redirect(SIGN_UP_URL)

def LogoutView(request):
    logout(request)
    # TODO - create message for logout user
    return redirect(LOGIN_REDIRECT_URL)

@method_decorator(login_required, name='dispatch')
class ProfileUser(View):
    template_name = 'accounts/profile.html'
    form_class = EditUserForm

    def get(self, request):
        std = Student.objects.get(user_id=request.user.pk)
        context = {
            'user_form': self.form_class(instance = request.user),
            'std_form': EditStudentForm(instance = std),}
        return render(request, self.template_name, context)

    def post(self, request):
        old_photo_name = None
        if request.user.student.student_image.name:
            old_photo_path = request.user.student.student_image.path
            old_photo_name = request.user.student.student_image.name
        edit_user = self.form_class(request.POST, instance = request.user)
        edit_std = EditStudentForm(request.POST, request.FILES, instance = request.user.student)
        if edit_std.is_valid():
            new_profile_image = edit_std.cleaned_data.get('student_image')
            if new_profile_image and new_profile_image.name != old_photo_name:
                if old_photo_name:
                    os.remove(old_photo_path)
            else:
                edit_std.cleaned_data['student_image'] = None
            edit_std.save()
        if edit_user.is_valid():
            edit_user.save()
            # TODO - sweetify.toast(request, 'Edit successfully', 'success')
        else:
            # TODO - sweetify.toast(request, 'Edit failed', 'warning')
            pass
        return redirect('/account/profile/')


@login_required
def delete_photo(request):
    std_image = request.user.student
    if request.method == 'GET':
        if std_image.student_image:
            std_image.student_image.delete()
            std_image.student_image = None
            std_image.save()
            # TODO - sweetify.toast(request, 'image profile deleted', 'success')
            return redirect('/account/profile/')
        else:
            # TODO - sweetify.toast(request, "don't have image profile", 'error')
            return redirect('/account/profile/')
    else:
        # TODO - sweetify.toast(request, 'remove image profile failed', 'error')
        return redirect('/account/profile/')