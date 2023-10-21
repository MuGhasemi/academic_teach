from django.urls import path
from .views import LoginView, RegisterView,  ProfileUser, LogoutView, delete_photo

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', RegisterView.as_view(), name='sign_up'),
    path('logout/', LogoutView, name='logout'),

    path('profile/', ProfileUser.as_view(), name='profile'),
    path('profile/delete-photo/', delete_photo, name='delete_photo'),
]