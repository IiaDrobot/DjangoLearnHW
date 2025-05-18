from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    page_size = 6
    ordering = 'id'

class SubTaskPagination(PageNumberPagination):
   page_size = 5
   ordering = '-created_at'





