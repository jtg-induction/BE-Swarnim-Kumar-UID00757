from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name='todos'
    )
    name = models.CharField(max_length=1000)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
