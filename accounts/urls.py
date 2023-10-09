from django.urls import path
from .views import LoginView, RegisterView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', RegisterView.as_view(), name='sign_up'),
    path('logout/', LogoutView, name='logout')
]