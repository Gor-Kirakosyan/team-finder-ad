from django import forms
from django.core.exceptions import ValidationError
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название проекта',
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание проекта',
                'rows': 5,
                'class': 'form-textarea',
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/username/repository',
                'class': 'form-input',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'name': 'Название:',
            'description': 'Описание:',
            'github_url': 'Ссылка на GitHub:',
            'status': 'Статус:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['status'].required = True

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise ValidationError("Ссылка должна вести на GitHub")
        return url
