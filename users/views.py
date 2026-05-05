from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse

from .models import User
from .forms import RegisterForm, LoginForm, EditProfileForm

from projects.views import paginate_queryset


FILTER_OWNERS_OF_FAVORITE_PROJECTS = 'owners-of-favorite-projects'
FILTER_OWNERS_OF_PARTICIPATING_PROJECTS = 'owners-of-participating-projects'
FILTER_INTERESTED_IN_MY_PROJECTS = 'interested-in-my-projects'
FILTER_PARTICIPANTS_OF_MY_PROJECTS = 'participants-of-my-projects'


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('project_list'))
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
            return redirect(reverse('project_list'))
        form.add_error(None, "Неверный имейл или пароль")
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('project_list'))


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
            return redirect(reverse('user_detail', kwargs={'pk': request.user.id}))
        return render(request, 'users/edit_profile.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.id})


class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        filter_param = request.GET.get('filter')
        active_filter = filter_param

        if request.user.is_authenticated and filter_param:
            if filter_param == FILTER_OWNERS_OF_FAVORITE_PROJECTS:
                users = User.objects.filter(
                    owned_projects__in=request.user.favorites.all()
                ).distinct()
            elif filter_param == FILTER_OWNERS_OF_PARTICIPATING_PROJECTS:
                users = User.objects.filter(
                    owned_projects__in=request.user.participated_projects.all()
                ).distinct()
            elif filter_param == FILTER_INTERESTED_IN_MY_PROJECTS:
                users = User.objects.filter(
                    favorites__in=request.user.owned_projects.all()
                ).distinct()
            elif filter_param == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
                users = User.objects.filter(
                    participated_projects__in=request.user.owned_projects.all()
                ).distinct()

        participants = paginate_queryset(request, users)

        return render(request, 'users/participants.html', {
            'participants': participants,
            'active_filter': active_filter,
        })
