from datetime import timedelta
from django.utils import timezone
from task_hw8.models import Task, SubTask



task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3)
)


subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    task=task,
    status="New",
    deadline=timezone.now() + timedelta(days=2)
)


subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    task=task,
    status="New",
    deadline=timezone.now() + timedelta(days=1)
)


new_tasks = Task.objects.filter(status="New")
print("Tasks with status 'New':", new_tasks)


overdue_done_subtasks = SubTask.objects.filter(status="Done", deadline__lt=timezone.now())
print("Overdue done SubTasks:", overdue_done_subtasks)


task.status = "In progress"
task.save()

subtask1.deadline = timezone.now() - timedelta(days=2)
subtask1.save()

subtask2.description = "Create and format presentation slides"
subtask2.save()


task.delete()
