from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginUserForm
from .models import Student
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from config.settings import LOGIN_URL

class LoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginUserForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)
    # TODO - fix login for teachers
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                _ = Student.objects.get(email=email)
                valid_password = check_password(password, _.password)
                if valid_password:
                    request.session['std_id'] = str(_.student_id)
                    # TODO - create message for login successfully
                    return redirect('/')
                # TODO - create message for login failed
                return redirect(LOGIN_URL)
            except ObjectDoesNotExist:
                _ = None
        # TODO - create message for login failed
        return redirect(LOGIN_URL)
