from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        paginator = Paginator(projects, 12)
        page_number = request.GET.get('page')
        projects_page = paginator.get_page(page_number)
        return render(request, 'projects/project_list.html', {'projects': projects_page})


class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
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
            return redirect(f'/projects/{project.id}/')
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


class ProjectEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return redirect(f'/projects/{pk}/')
        form = ProjectForm(instance=project)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})
    
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return redirect(f'/projects/{pk}/')
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(f'/projects/{pk}/')
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


class ProjectCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user == project.owner and project.status == 'open':
            project.status = 'closed'
            project.save()
            return JsonResponse({'status': 'ok', 'project_status': 'closed'})
        return JsonResponse({'status': 'error'}, status=400)


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project in request.user.favorites.all():
            request.user.favorites.remove(project)
            favorited = False
        else:
            request.user.favorites.add(project)
            favorited = True
        return JsonResponse({'status': 'ok', 'favorited': favorited})


class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.participants.all():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return JsonResponse({'status': 'ok'})


class FavoriteProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        projects = request.user.favorites.all().order_by('-created_at')
        paginator = Paginator(projects, 12)
        page_number = request.GET.get('page')
        projects_page = paginator.get_page(page_number)
        return render(request, 'projects/favorite_projects.html', {'projects': projects_page})