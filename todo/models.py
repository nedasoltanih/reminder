from django.db import models
from django.utils import timezone

from todo.managers import AliManager, TaskManager, UserManager


class User(models.Model):
    name = models.CharField(null=True, max_length=200)
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    objects = UserManager()


class Task(models.Model):
    category_choices = [
        ('j', 'Job'),
        ('h', 'Hobby'),
        ('s', 'School')
    ]
    title = models.CharField(null=True, max_length=200
                             , verbose_name="Task title", db_column="name")
    category = models.CharField(choices=category_choices, max_length=1)

    due_date = models.DateTimeField(default=timezone.now,
                                    help_text="The time and date in which the task must be done!")
    creation_date = models.DateTimeField(editable=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = TaskManager()
    ali_tasks = AliManager()

    def __str__(self):
        return self.title

    def due_date_passed(self):
        return self.due_date > timezone.now()


class Project(models.Model):
    title = models.CharField(null=True, max_length=200
                             , verbose_name="Project title")
    hours = models.IntegerField(default=1)
    logo = models.ImageField(upload_to='images', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    task = models.ManyToManyField(Task)
