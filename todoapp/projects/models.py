
from django.db import models


class Project(models.Model):
    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)
        Add string representation for this model with project name.
    """
    class Status(models.IntegerChoices):
        TO_BE_STARTED = 0, "To be started"
        IN_PROGRESS = 1, "In progress"
        COMPLETED = 2, "Completed"
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        'users.CustomUser', through='ProjectMember', related_name='projects'
    )
    max_members = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.TO_BE_STARTED)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """
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


