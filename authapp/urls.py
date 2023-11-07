from django.urls import path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('accounts/register/', views.CreateUserView.as_view(), name='user-register'),
    path('accounts/login/', views.LoginView.as_view(), name='user-login'),
    path('accounts/profile/view/', views.ProfileView.as_view(), name='view-profile'),
    path('accounts/profile/edit/', views.ProfileUpdateView.as_view(), name='edit-profile'),
]