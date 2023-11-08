from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Task, User
from django.shortcuts import get_object_or_404
from django.views import View

def index(request):
    if request.method == "GET":
        return HttpResponse("Hello, world. You're at the todo index.")


class Index(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the todo index.")
    def post(self, request):
        pass


def task_detail(request, task_id=1):
    # task = Task.objects.get(pk=task_id)
    task = get_object_or_404(Task, pk=task_id)
    template = loader.get_template('todo/detail.html')
    return HttpResponse(template.render({'task': task}, request))


class TaskDetail(DetailView):
    model = Task


def list(request):
    tasks = Task.objects.all()
    # output = ",".join([t.title for t in tasks])
    template = loader.get_template('todo/all.html')
    return HttpResponse(template.render({'all_tasks': tasks, "title": "All tasks"}, request))


class ListTasks(ListView):
    model = Task


class ListUsers(ListView):
    model = User


def new_task(request):
    if request.method == "GET":
        template = loader.get_template('todo/new_task.html')
        return HttpResponse(template.render({}, request))

    elif request.method == "POST":
        try:
            task = Task(title=request.POST["title"],
                    category=request.POST["category"],
                    due_date=request.POST["due_date"])
            task.save()
            return HttpResponse("saved successfully")
        except:
            return HttpResponse("Something went wrong!")


class NewTask(View):
    def get(self, request, *args, **kwargs):
        # print(args)
        # print(kwargs)
        # print(request.GET)
        template = loader.get_template('todo/new_task.html')
        return HttpResponse(template.render({}, request))

    def post(self, request, *args, **kwargs):
        # print(args)
        # print(kwargs)
        # print(request.POST)
        try:
            task = Task(title=request.POST["title"],
                    category=request.POST["category"],
                    due_date=request.POST["due_date"])
            task.save()
            return HttpResponse("saved successfully")
        except:
            return HttpResponse("Something went wrong!")


class EditTask(View):
    def get(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(pk=kwargs['pk'])
            template = loader.get_template('todo/new_task.html')
            return HttpResponse(template.render({"task":task}, request))
        except Task.DoesNotExist:
            template = loader.get_template('todo/404.html')
            return HttpResponse(template.render({}, request))

    def post(self, request, *args, **kwargs):
        # try:
            task = Task.objects.filter(pk=kwargs['pk'])
            if task:
                task[0].title = request.POST["title"]
                task[0].category = request.POST["category"]
                task[0].due_date = request.POST["due_date"]
                task[0].save()
                return HttpResponse("updated successfully")
            else:
                template = loader.get_template('todo/404.html')
                return HttpResponse(template.render({}, request))
        # except:
        #     return HttpResponse("Something went wrong!")