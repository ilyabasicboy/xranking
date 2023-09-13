# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Project, ProjectQuery, Query, SearchResult, ProjectResult
from django_admin_inline_paginator.admin import TabularInlinePaginated


class ProjectQueryInline(TabularInlinePaginated):
    model = ProjectQuery
    extra = 0
    per_page = 15


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    model = Query
    list_per_page = 10
    search_fields = ['query']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [ProjectQueryInline]
    list_per_page = 10


admin.site.register(ProjectQuery)
admin.site.register(SearchResult)
admin.site.register(ProjectResult)