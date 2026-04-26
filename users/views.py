from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from .models import User
from .forms import RegisterForm, LoginForm, EditProfileForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/projects/list/')
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/projects/list/')
        form.add_error(None, "Неверный имейл или пароль")
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/projects/list/')


class UserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'users/user-details.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'users/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f'/users/{request.user.id}/')
        return render(request, 'users/edit_profile.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return f'/users/{self.request.user.id}/'


class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        filter_param = request.GET.get('filter')
        active_filter = filter_param

        if request.user.is_authenticated and filter_param:
            if filter_param == 'owners-of-favorite-projects':
                users = User.objects.filter(
                    owned_projects__in=request.user.favorites.all()).distinct()
            elif filter_param == 'owners-of-participating-projects':
                users = User.objects.filter(
                    owned_projects__in=request.user.participated_projects.all()).distinct()
            elif filter_param == 'interested-in-my-projects':
                users = User.objects.filter(
                    favorites__in=request.user.owned_projects.all()).distinct()
            elif filter_param == 'participants-of-my-projects':
                users = User.objects.filter(
                    participated_projects__in=request.user.owned_projects.all()).distinct()

        paginator = Paginator(users, 12)
        page_number = request.GET.get('page')
        participants = paginator.get_page(page_number)

        return render(request, 'users/participants.html', {
            'participants': participants,
            'active_filter': active_filter,
        })
