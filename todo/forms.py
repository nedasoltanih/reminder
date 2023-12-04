from django import forms
from django.contrib.auth.models import User

from todo.models import Task, Student


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class NameForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=40, widget=forms.Textarea)
    email = forms.EmailField()
    image = forms.ImageField(required=False)


# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ["first_name", "last_name", "username", "password", "email"]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["std_no"]


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]
