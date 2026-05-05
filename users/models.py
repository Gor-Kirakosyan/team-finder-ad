from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, URLValidator
from django.utils import timezone

from .managers import CustomUserManager
from .utils import generate_avatar_from_initials, normalize_phone


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="адрес электронной почты",
        unique=True,
        error_messages={"unique": "Пользователь с таким email уже существует"},
    )
    name = models.CharField(verbose_name="имя", max_length=124)
    surname = models.CharField(verbose_name="фамилия", max_length=124)
    avatar = models.ImageField(
        verbose_name="аватар",
        upload_to="avatars/",
        blank=True,
        null=True
    )
    phone = models.CharField(
        verbose_name="номер телефона",
        max_length=12,
        validators=[
            RegexValidator(
                regex=r"^(\+7|8)\d{10}$",
                message="Номер телефона должен быть в формате 8xxxxxxxxxx или +7xxxxxxxxxx"
            ),
        ],
    )
    github_url = models.URLField(
        verbose_name="ссылка на GitHub",
        blank=True,
        null=True,
        validators=[URLValidator()]
    )
    about = models.TextField(
        verbose_name="описание профиля",
        max_length=256,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name="активный пользователь", default=True)
    is_staff = models.BooleanField(verbose_name="администратор", default=False)
    date_joined = models.DateTimeField(
        verbose_name="дата регистрации", default=timezone.now)
    favorites = models.ManyToManyField(
        'projects.Project',
        verbose_name="избранные проекты",
        blank=True,
        related_name="favorited_by"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            avatar_content = generate_avatar_from_initials(
                self.name, self.surname)
            self.avatar.save(
                f"avatar_{self.name}_{self.surname}.png",
                avatar_content,
                save=False
            )

        if self.phone:
            self.phone = normalize_phone(self.phone)

        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def get_short_name(self):
        return self.name
