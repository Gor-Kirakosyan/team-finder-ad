from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email должен быть указан"))
        if not name:
            raise ValueError(_("Имя должно быть указано"))
        if not surname:
            raise ValueError(_("Фамилия должна быть указана"))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_superuser=True"))

        return self.create_user(email, name, surname, password, **extra_fields)