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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from task_hw8.views import LogOutAPIView
from rest_framework_simplejwt.views import (TokenBlacklistView)



schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/', greetings),

    path('tasks/create/', create_task, name='task-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-update-delete'),
    path('tasks/stats/', task_statistics, name='task-stats'),
    path('tasks/by-weekday/', get_tasks_by_weekday, name='task-by-weekday'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/list/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail-update-delete'),

    path('api/', include(router.urls)),
    path('test-log/', test_log, name='test_log'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Swagger:
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui()),
    path('swagger/', schema_view.with_ui('swagger')),
    path('redoc/', schema_view.with_ui('redoc')),
    path('api/logout/', LogOutAPIView.as_view(), name='logout'),
    path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),


]








