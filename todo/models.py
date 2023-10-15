from django.db import models


class Task(models.Model):
    title = models.CharField(null=True, max_length=200
                             ,verbose_name="Task title")
    category = models.CharField(choices=[
        ('j','Job'),
        ('h','Hobby'),
        ('s','School')
    ], max_length=1)
