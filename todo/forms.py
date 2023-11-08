from django.forms import ModelForm
from todo.models import Task


class TaskForm(ModelForm):
    class meta:
        model = Task