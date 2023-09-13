from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):

    domain = models.CharField(
        max_length=255
    )
    active = models.BooleanField(
        default=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.domain


class ProjectQuery(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_queries'
    )
    query = models.OneToOneField(
        'Query',
        on_delete=models.CASCADE,
    )
    frequency = models.CharField(
        max_length=255,
        default='1'
    )
    depts = models.CharField(
        max_length=255,
        default='100'
    )

    def __str__(self):
        return '%s - %s' % (self.project.domain, self.query.query)


class Query(models.Model):

    query = models.TextField()
    region = models.CharField(
        max_length=255
    )
    search_engine = models.CharField(
        max_length=255,
        default='google'
    )

    def __str__(self):
        return self.query


class SearchResult(models.Model):

    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        default=timezone.now
    )
    domain = models.CharField(
        max_length=255
    )
    url = models.CharField(
        max_length=255
    )
    position = models.PositiveIntegerField()

    def __str__(self):
        return '%s - %s' % (self.date, self.query)


class ProjectResult(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        default=timezone.now
    )
    url = models.CharField(
        max_length=255
    )
    query = models.ForeignKey(
        'Query',
        on_delete=models.CASCADE,
        related_name='project_results'
    )
    position = models.PositiveIntegerField()

    def __str__(self):
        return '%s - %s' % (self.date, self.project.domain)