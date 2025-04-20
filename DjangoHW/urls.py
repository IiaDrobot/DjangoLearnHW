"""
URL configuration for DjangoHW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from greetings.views import greetings
from task_hw8.views import (
    task_crud_view,
    create_task,
    get_all_tasks,
    get_task_by_id,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView
)
from django.urls import path
from task_hw8.views import get_tasks_by_weekday
from task_hw8.views import SubTaskListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/', greetings),
    path('task-crud/', task_crud_view),


    path('tasks/create/', create_task, name='task-create'),
    path('tasks/', get_all_tasks, name='task-list'),
    path('tasks/<int:pk>/', get_task_by_id, name='task-detail'),
    path('tasks/stats/', task_statistics, name='task-stats'),


    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks/by-weekday/', get_tasks_by_weekday, name='task-by-weekday'),
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),



]











