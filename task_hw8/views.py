
from django.shortcuts import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Task, SubTask

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





# Create your views here.
