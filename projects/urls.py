from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('create-project/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('<int:pk>/complete/', views.ProjectCompleteView.as_view(), name='project_complete'),
    path('<int:pk>/toggle-favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('<int:pk>/toggle-favorite/',
         views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('favorites/', views.FavoriteProjectsView.as_view(), name='favorite_projects'),
]
