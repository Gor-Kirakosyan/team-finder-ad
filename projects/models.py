from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.utils import timezone


class Project(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("closed", "Закрыт"),
    ]

    name = models.CharField(verbose_name="название проекта", max_length=200)
    description = models.TextField(verbose_name="описание проекта", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="автор проекта",
                              on_delete=models.CASCADE, related_name="owned_projects")
    created_at = models.DateTimeField(verbose_name="дата создания проекта", default=timezone.now)
    github_url = models.URLField(verbose_name="ссылка на GitHub",
                                 blank=True, null=True, validators=[URLValidator()])
    status = models.CharField(verbose_name="статус проекта", max_length=6,
                              choices=STATUS_CHOICES, default="open")
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="участники проекта",
        blank=True,
        related_name="participated_projects"
    )

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def is_open(self):
        return self.status == "open"

    def can_user_edit(self, user):
        return user == self.owner

    def add_participant(self, user):
        if user not in self.participants.all():
            self.participants.add(user)

    def remove_participant(self, user):
        if user in self.participants.all():
            self.participants.remove(user)

    def complete(self):
        if self.status == "open":
            self.status = "closed"
            self.save()
