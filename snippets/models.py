from __future__ import unicode_literals

# Django
from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    '''Language attributes'''

    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        """Return name."""
        return '{}'.format(self.name)


class Snippet(models.Model):
    '''Snippet attributes'''

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    snippet = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=False)

    # Audit control
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Object relations
    language = models.ForeignKey('snippets.Language', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    def __str__(self):
        """Return name."""
        return '{}'.format(self.name)
