from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .forms import NameForm, TaskForm
from .models import Task, User
from django.shortcuts import get_object_or_404, redirect, render
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
            return HttpResponse(template.render({"task": task}, request))
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


class Login(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('todo/login.html')
        return HttpResponse(template.render({}, request))

    def post(self, request, *args, **kwargs):
        usernames = User.objects.values_list("username")
        for user in usernames:
            if request.POST["username"] == user[0]:
                user_info = User.objects.filter(username=user[0]).values_list("id", "password")
                # print(request.POST["password"])
                # print(password)
                if request.POST["password"] == user_info[0][1]:
                    # message = "Login successful!"
                    return redirect(f"/todo/user_tasks/{user_info[0][0]}/")
                else:
                    message = "Wrong password!"
                break
        else:
            message = "User not found!"

        template = loader.get_template('todo/login.html')
        return HttpResponse(template.render({'message': message}, request))


class UserTasks(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=kwargs['pk'])
        template = loader.get_template('todo/all.html')
        return HttpResponse(template.render({'all_tasks': tasks, "title": "All tasks"}, request))


class Name(View):
    def get(self, request):
        form = NameForm()
        print(form.is_bound)
        return render(request, "todo/get_name.html", {'form':form})

    def post(self, request):
        form = NameForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponse("Saved!")
        else:
            print(form.errors)
            return HttpResponse("Not saved!")


class AddTask(View):
    def get(self, request):
        form = TaskForm()
        return render(request, "todo/add_task.html", {"form":form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            # task = Task(title=form.cleaned_data["title"],
            #             category=form.cleaned_data["category"],
            #             due_date=form.cleaned_data["due_date"],
            #             user=form.cleaned_data["user"])
            # task.save()
            form.save()
            return HttpResponse("Saved!")
        else:
            return render(request, "todo/add_task.html", {"form": form})