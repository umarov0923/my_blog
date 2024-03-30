from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View

from post.models import Post
from .forms import UserCreateForm, UserUpdateForm
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'users/register_user.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, 'users/register_user.html', {'form': form})


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            return redirect('post:post-list')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('post:post-list')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().filter(user=request.user)
        return render(request, 'users/profile.html', {'posts': posts})


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': form})

    def post(self, request):
        form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('users:profile')
        return render(request, 'users/profile_edit.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
        }
        )


