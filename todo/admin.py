from django.contrib import admin

from .models import Task, Project, Student

admin.site.register(Task)
admin.site.register(Project)
# admin.site.register(User)
# admin.site.register(Person)
admin.site.register(Student)
