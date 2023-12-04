from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser

from reminder import settings
from todo.managers import AliManager, TaskManager, PersonManager
import logging

# class User(models.Model):
#     name = models.CharField(null=True, max_length=200)
#     username = models.CharField(max_length=20, null=True)
#     password = models.CharField(max_length=20, null=True)
#
#     def __str__(self):
#         return self.name
#
#     objects = UserManager()


"""Proxy model"""
# class Person(User):
#     people = PersonManager()
#
#     class Meta:
#         proxy = True


"""one to one"""
class Student(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    std_no = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.std_no} - {self.django_user.first_name} {self.django_user.last_name}"


# class MyUser1(AbstractBaseUser, PermissionsMixin):
#     phone = models.CharField(max_length=11, unique=True)
#     first_name = models.CharField(max_length=20)
#     is_active = models.BooleanField('active', default=True)
#
#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = ['phone']
#
#     def get_full_name(self):
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
#
#     def get_short_name(self):
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         send_mail(subject, message, from_email, [self.email], **kwargs)
#
#
# class MyUser2(AbstractUser):
#     bio = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.first_name




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
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    objects = TaskManager()
    ali_tasks = AliManager()

    def __str__(self):
        return self.title

    def due_date_passed(self):
        passed = self.due_date > timezone.now()
        if passed:
            send_mail(
                subject = f'Your task {self.title} is due',
                message = f'Your task {self.title} is due',
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [self.user.django_user.email]
            )

        return passed

    def save(self):
        super().save()
        logging.getLogger("file_logger").warning("a task instance created.")



class Project(models.Model):
    title = models.CharField(null=True, max_length=200
                             , verbose_name="Project title")
    hours = models.IntegerField(default=1)
    logo = models.ImageField(upload_to='images', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    task = models.ManyToManyField(Task)
