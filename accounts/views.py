from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginUserForm, RegisterUserForm
from .models import User, Student
from django.contrib.auth import authenticate, login
from config.settings import LOGIN_URL, LOGIN_REDIRECT_URL, SIGN_UP_URL

class LoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginUserForm

    def get(self, request):
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
