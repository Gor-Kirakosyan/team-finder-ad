from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.utils import timezone

MAX_NAME_LENGTH = 200


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Открыт"),
        (STATUS_CLOSED, "Закрыт"),
    ]

    name = models.CharField(
        verbose_name="Название проекта",
        max_length=MAX_NAME_LENGTH
    )
    description = models.TextField(
        verbose_name="Описание проекта",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор проекта",
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания проекта",
        default=timezone.now
    )
    github_url = models.URLField(
        verbose_name="Ссылка на GitHub",
        blank=True,
        null=True,
        validators=[URLValidator()]
    )
    status = models.CharField(
        verbose_name="Статус проекта",
        max_length=6,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Участники проекта",
        blank=True,
        related_name="participated_projects"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
