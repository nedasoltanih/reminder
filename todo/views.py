from django.template import loader
from django.http import HttpResponse
from .models import Task
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


def list(request):
    tasks = Task.objects.all()
    # output = ",".join([t.title for t in tasks])
    template = loader.get_template('todo/all.html')
    return HttpResponse(template.render({'all_tasks': tasks}, request))