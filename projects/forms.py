from django import forms
from django.core.exceptions import ValidationError

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название проекта'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Опишите ваш проект...', 'rows': 5}
            ),
            'github_url': forms.URLInput(
                attrs={'placeholder': 'https://github.com/username/repository'}
            ),
            'status': forms.Select(),
        }
        labels = {
            'name': 'Название:',
            'description': 'Описание:',
            'github_url': 'Ссылка на GitHub:',
            'status': 'Статус:',
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise ValidationError("Ссылка должна вести на GitHub")
        return url
