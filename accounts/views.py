from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login
from config.settings import LOGIN_URL, LOGIN_REDIRECT_URL

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

