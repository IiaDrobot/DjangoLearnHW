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
from django.urls import path, include
from greetings.views import greetings
from task_hw8.views import (
    #task_crud_view,
    create_task,
    get_all_tasks,
    get_task_by_id,
    task_statistics,
    SubTaskListView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    get_tasks_by_weekday,
    CategoryViewSet,
    test_log,
)

from rest_framework.routers import DefaultRouter

from django.urls import path
from task_hw8 import views
from task_hw8.views import test_log
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/', greetings),
   # path('task-crud/', task_crud_view),

    path('tasks/create/', create_task, name='task-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-update-delete'),
    path('tasks/stats/', task_statistics, name='task-stats'),
    path('tasks/by-weekday/', get_tasks_by_weekday, name='task-by-weekday'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/list/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail-update-delete'),


    path('api/', include(router.urls)),

    path('test-log/', views.test_log, name='test_log'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]









