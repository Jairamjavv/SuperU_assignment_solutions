from django.urls import path, include
from .views import Register, LoginView, LogoutView
from . import views

urlpatterns = [
    path('register',Register.as_view()),
    path('login',LoginView.as_view()),
    path('logout',LogoutView.as_view()),
    path('user_profiles/', views.users_list, name='users_list'),
    path('update_user_profile/<int:id>/', views.update_user_profile, name='update_user_profile'),
]
