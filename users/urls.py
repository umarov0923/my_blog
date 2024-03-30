from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, \
    UpdateProfileView, change_password

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', UpdateProfileView.as_view(), name='profile_edit'),
    path('password_change/', change_password, name='password_change')

]