from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home1/", views.index, name="home1"),
    path("home2/", views.Index.as_view(), name="home2"),
    # path("<int:task_id>/", views.task_detail, name="task_detail"),
    path("<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    path("all/", views.ListTasks.as_view(), name="all"),
    path("ali/", views.list, name="ali"),
    # path("new_task/", views.new_task, name="new_task"),
    path("new_task/", views.NewTask.as_view(), name="new_task"),
    path("edit_task/<int:pk>/", views.EditTask.as_view(), name="edit_task"),
    path("all_users/", views.ListUsers.as_view(), name="all_users"),
    path("login/", views.Login.as_view(), name="login"),
    path("user_tasks/<int:pk>/", views.UserTasks.as_view(), name="user_tasks"),
    path("name/", views.Name.as_view(), name="name"),
    path("add_task/", views.AddTask.as_view(), name="add_task"),
    path("no_task/", views.NoTask.as_view(), name="no_task")
]