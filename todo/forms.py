from django import forms
from todo.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class NameForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=40, widget=forms.Textarea)
    email = forms.EmailField()
    image = forms.ImageField(required=False)
