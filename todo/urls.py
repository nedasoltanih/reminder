from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home1/", views.index, name="home1"),
    path("home2/", views.Index.as_view(), name="home2"),
    path("<int:task_id>/", views.task_detail, name="task_detail"),
    path("all/", views.list, name="home"),
]