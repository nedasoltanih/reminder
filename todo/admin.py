from django.contrib import admin

from .models import Task, Project, User

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(User)
