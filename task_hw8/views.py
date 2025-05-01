from django.shortcuts import HttpResponse
from django.utils import timezone
from datetime import timedelta
from collections import Counter
import calendar

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractWeekDay

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)
from .pagination import SubTaskPagination


# Task Views
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


#  SubTask Views
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class SubTaskListView(ListAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_title = self.request.query_params.get('task')
        status = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if status:
            queryset = queryset.filter(status__iexact=status)

        return queryset


#  API Views
@api_view(['GET'])
def get_tasks_by_weekday(request):
    weekday_name = request.query_params.get('weekday', None)

    if weekday_name:
        weekdays_map = {day.lower(): index for index, day in enumerate(calendar.day_name, start=0)}
        weekday_num = weekdays_map.get(weekday_name.lower())

        if weekday_num is None:
            return Response({'error': 'Некорректное имя дня недели'}, status=400)

        drf_weekday_num = (weekday_num + 1) % 7 + 1

        tasks = Task.objects.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=drf_weekday_num)
    else:
        tasks = Task.objects.all()

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def create_task(request):
    if request.method == 'GET':
        return Response({'message': 'Отправь POST-запрос с данными задачи'})

    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task_by_id(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
def task_statistics(request):
    tasks = Task.objects.all()
    total_tasks = tasks.count()
    status_counts = Counter(tasks.values_list('status', flat=True))
    overdue_tasks = tasks.filter(deadline__lt=timezone.now()).exclude(status='Done').count()

    return Response({
        'total_tasks': total_tasks,
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks
    })


def task_crud_view(request):
    task, created = Task.objects.get_or_create(
        title="Prepare presentation",
        defaults={
            "description": "Prepare materials and slides for the presentation",
            "status": "New",
            "deadline": timezone.now() + timedelta(days=3),
        }
    )

    SubTask.objects.get_or_create(
        title="Gather information",
        defaults={
            "description": "Find necessary information for the presentation",
            "task": task,
            "status": "New",
            "deadline": timezone.now() + timedelta(days=2),
        }
    )

    SubTask.objects.get_or_create(
        title="Create slides",
        defaults={
            "description": "Create presentation slides",
            "task": task,
            "status": "New",
            "deadline": timezone.now() + timedelta(days=1),
        }
    )

    new_tasks = Task.objects.filter(status="New")
    overdue_done_subtasks = SubTask.objects.filter(status="Done", deadline__lt=timezone.now())

    task.status = "In progress"
    task.save()

    subtask1 = SubTask.objects.get(title="Gather information")
    subtask1.deadline = timezone.now() - timedelta(days=2)
    subtask1.save()

    subtask2 = SubTask.objects.get(title="Create slides")
    subtask2.description = "Create and format presentation slides"
    subtask2.save()

    task.delete()

    return HttpResponse("CRUD операции выполнены.")



# class SubTaskListCreateView(APIView):
#     def get(self, request):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskSerializer(subtasks, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get_object(self, pk):
#         try:
#             return SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return None
#
#     def get(self, request, pk):
#         subtask = self.get_object(pk)
#         if not subtask:
#             return Response({'error': 'Подзадача не найдена'}, status=404)
#         serializer = SubTaskSerializer(subtask)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         subtask = self.get_object(pk)
#         if not subtask:
#             return Response({'error': 'Подзадача не найдена'}, status=404)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, pk):
#         subtask = self.get_object(pk)
#         if not subtask:
#             return Response({'error': 'Подзадача не найдена'}, status=404)
#         subtask.delete()
#         return Response(status=204)

