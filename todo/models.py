import datetime
from django.db import models


class User(models.Model):
    name = models.CharField(null=True, max_length=200)
    def __str__(self):
        return self.name


class Task(models.Model):
    category_choices = [
        ('j','Job'),
        ('h','Hobby'),
        ('s','School')
    ]
    title = models.CharField(null=True, max_length=200
                             ,verbose_name="Task title", db_column="name")
    category = models.CharField(choices=category_choices, max_length=1)

    due_date = models.DateTimeField(default=datetime.datetime.now(),
                                    help_text="The time and date in which the task must be done!")
    creation_date = models.DateTimeField(editable=False, default=datetime.datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(null=True, max_length=200
                             ,verbose_name="Project title")
    hours = models.IntegerField(default=1)
    logo = models.ImageField(upload_to='images', null=True, blank=True)
    website = models.URLField(null=True, blank=True)





