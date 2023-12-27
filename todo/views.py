from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView

from .forms import NameForm, TaskForm, StudentForm, UserForm
from .models import Task, Student
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# from django.contrib.auth.models import User
# from .models import Person
import logging
logger1 = logging.getLogger(__name__)
logger2 = logging.getLogger("file_logger")


def index(request):
    logger2.error("index page is browsed!")
    # request.session['fav_color'] = 'blue'
    print(request.COOKIES)
    if request.method == "GET":
        return HttpResponse("Hello, world. You're at the todo index.")


class Index(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the todo index.")

    def post(self, request):
        pass


def task_detail(request, task_slug=""):
    # task = Task.objects.get(pk=task_id)
    try:
        task = Task.objects.get(slug=task_slug)
        template = loader.get_template('todo/detail.html')
        return HttpResponse(template.render({'task': task}, request))
    except:
        logger2.warning(f"Task with id {task_slug} not found!")
        template = loader.get_template('todo/404.html')
        return HttpResponse(template.render({}, request))

class TaskDetail(DetailView):
    model = Task


def list(request):
    tasks = Task.ali_tasks.all()
    # tasks = Task.objects.filter(user=1)
    # output = ",".join([t.title for t in tasks])
    template = loader.get_template('todo/all.html')
    return HttpResponse(template.render({'all_tasks': tasks, "title": "All tasks"}, request))


class ListTasks(ListView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListTasks, self).get_context_data()
        # context["color"] = self.request.session.get("color","black")
        context["color"] = self.request.COOKIES.get("color","black")
        return context

    def post(self, request):
        # request.session["color"] = request.POST["color"]
        response = super().get(request)
        response.set_cookie("color", request.POST["color"])
        return response



class ListUsers(PermissionRequiredMixin, ListView):
    permission_required = "django.contrib.auth.view_user"
    # model = Person


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
        except Exception as e:
            logger2.error(f"Error occured while creating task: {e}")
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
        # usernames = User.objects.values_list("username")
        # for user in usernames:
        #     if request.POST["username"] == user[0]:
        #         user_info = User.objects.filter(username=user[0]).values_list("id", "password")
        #         # print(request.POST["password"])
        #         # print(password)
        #         if request.POST["password"] == user_info[0][1]:
        #             message = "Login successful!"
        #             request.session["user"] = user[0]
        #             return redirect(f"/todo/user_tasks/{user_info[0][0]}/")
        #         else:
        #             message = "Wrong password!"
        #         break
        # else:
        #     message = "User not found!"

        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            message = "Login successful!"
            if request.GET.get("next", None):
                return redirect(request.GET["next"])
        else:
            message = "User not found or wrong password!"

        template = loader.get_template('todo/login.html')
        response = HttpResponse(template.render({'message': message}, request))
        response.set_cookie("last_login", str(datetime.now()))
        return response


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "todo/logout.html")
        else:
            return redirect("login")

    def post(self, request):
        logout(request)
        return HttpResponse("Logout successful!")


class UserTasks(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/todo/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'todo.view_tasks'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=kwargs['pk'])
        template = loader.get_template('todo/all.html')
        last = request.COOKIES.get("last_login", None)
        return HttpResponse(template.render({'all_tasks': tasks, "last_login": last}, request))

# http://127.0.0.1:8000/todo/login/?next=/todo/user_tasks/1/

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
            logger1.warning(f"Task is not created: {form.errors}")
            return render(request, "todo/add_task.html", {"form": form})


# class NoTask(ListView):
#     model = Person
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         return {"object_list": Person.objects.users_with_no_task()}


# class Register(View):
#     def get(self, request):
#         form = PersonForm()
#         return render(request, "todo/register.html", {"form":form})
#
#     def post(self, request):
#         form = PersonForm(request.POST)
#         if form.is_valid():
#             # form.cleaned_data["is_active"] = False
#             form.save()
#             return HttpResponse("Success!")
#         else:
#             return render(request, "todo/register.html", {"form": form})

class RegisterStudent(View):
    def get(self, request):
        form1 = StudentForm()
        form2 = UserForm()
        return render(request, "todo/register_std.html", {"form1": form1, "form2":form2})

    def post(self, request):
        form1 = StudentForm()
        std = request.POST["std_no"]
        form2 = UserForm(request.POST)
        if form2.is_valid():
            # form.cleaned_data["is_active"] = False
            # form2.save()
            user = User.objects.create_user(request.POST)
            user.save()
            # get id of this user and add to django_user field in student
            # user = User.objects.latest("id")
            student = Student(std_no=std)
            student.save()
            return HttpResponse("Success!")
        else:
            return render(request, "todo/register_std.html", {"form1": form1, "form2":form2})