
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        'users.CustomUser', through='ProjectMember', related_name='projects'
    )
    max_members = models.PositiveIntegerField()
    STATUS_CHOICES = [
        (0, 'To be started'),
        (1, 'In progress'),
        (2, 'Completed'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE, related_name='project_members'
    )
    member = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name='project_memberships'
    )

    class Meta:
        unique_together = ('project', 'member')

    def __str__(self):
        return f"{self.project.name} - {self.member.email}"


