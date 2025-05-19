from datetime import timedelta
from collections import Counter
import calendar
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractWeekDay

#from .models import Task, SubTask, Category
from task_hw8.models import Task, SubTask, Category

from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer
)
from .pagination import SubTaskPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        response = Response(status=status.HTTP_200_OK)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.data = {'message': 'Успешный выход'}
        return response





logger = logging.getLogger(__name__)


def test_log(request):
    logger.info('Тестовый запрос на /test-log/')
    return HttpResponse("Test log recorded.")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = Task.objects.filter(categories=category).count()
        return Response({'task_count': count})


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class SubTaskListCreateView(ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)


class SubTaskListView(ListAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = SubTask.objects.filter(owner=self.request.user).order_by('-created_at')
        task_title = self.request.query_params.get('task')
        status_param = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset


@api_view(['GET'])
def get_tasks_by_weekday(request):
    weekday_name = request.query_params.get('weekday', None)

    if weekday_name:
        weekdays_map = {day.lower(): idx for idx, day in enumerate(calendar.day_name)}
        weekday_num = weekdays_map.get(weekday_name.lower())
        if weekday_num is None:
            return Response({'error': 'Некорректное имя дня недели'}, status=400)

        drf_weekday_num = weekday_num + 1
        tasks = Task.objects.annotate(weekday=ExtractWeekDay('deadline'))\
                   .filter(weekday=drf_weekday_num, owner=request.user)
    else:
        tasks = Task.objects.filter(owner=request.user)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def create_task(request):
    if request.method == 'GET':
        return Response({'message': 'Отправь POST-запрос с данными задачи'})

    serializer = TaskCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.filter(owner=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task_by_id(request, pk):
    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
def task_statistics(request):
    tasks = Task.objects.filter(owner=request.user)
    total_tasks = tasks.count()
    status_counts = Counter(tasks.values_list('status', flat=True))
    overdue_tasks = tasks.filter(deadline__lt=timezone.now()).exclude(status='Done').count()

    return Response({
        'total_tasks': total_tasks,
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks
    })


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


