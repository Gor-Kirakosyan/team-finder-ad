from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Имя:',
            'surname': 'Фамилия:',
            'email': 'Email:',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Неверный email или пароль'


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'avatar': forms.ClearableFileInput(
                attrs={'class': 'form-file', 'style': 'display: none;'}
                ),
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Имя:',
            'surname': 'Фамилия:',
            'avatar': 'Аватар:',
            'about': 'О себе:',
            'phone': 'Телефон:',
            'github_url': 'GitHub:',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if phone.startswith('8'):
                phone = '+7' + phone[1:]
            if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
                raise ValidationError(
                    "Пользователь с таким номером телефона уже существует"
                )
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise ValidationError("Ссылка должна вести на GitHub")
        return url


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-input'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-input'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-input'})
        self.fields['old_password'].label = 'Текущий пароль:'
        self.fields['new_password1'].label = 'Новый пароль:'
        self.fields['new_password2'].label = 'Подтверждение пароля:'
