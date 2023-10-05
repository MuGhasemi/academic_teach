from django.urls import path
from .views import LoginView, RegisterView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', RegisterView.as_view(), name='sign_up'),
]