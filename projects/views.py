from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from http import HTTPStatus

from .models import Project
from .forms import ProjectForm


def paginate_queryset(request, queryset, items_per_page=12):
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.select_related(
            'owner').order_by('-created_at')
        projects_page = paginate_queryset(request, projects)
        return render(request, 'projects/project_list.html', {'projects': projects_page})


class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(
            Project.objects.select_related('owner'), pk=pk)
        return render(request, 'projects/project-details.html', {'project': project})


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('project_detail', pk=project.id)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


class ProjectEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return redirect('project_detail', pk=pk)
        form = ProjectForm(instance=project)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return redirect('project_detail', pk=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


class ProjectCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user == project.owner and project.status == Project.STATUS_OPEN:
            project.status = Project.STATUS_CLOSED
            project.save()
            return JsonResponse({'status': 'ok', 'project_status': project.status})
        return JsonResponse({'status': 'error'}, status=HTTPStatus.BAD_REQUEST)


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user.favorites.filter(pk=project.pk).exists():
            request.user.favorites.remove(project)
            favorited = False
        else:
            request.user.favorites.add(project)
            favorited = True
        return JsonResponse({'status': 'ok', 'favorited': favorited})


class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.participants.filter(pk=request.user.pk).exists():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return JsonResponse({'status': 'ok'})


class FavoriteProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        projects = request.user.favorites.all().order_by('-created_at')
        projects_page = paginate_queryset(request, projects)
        return render(request, 'projects/favorite_projects.html', {'projects': projects_page})
