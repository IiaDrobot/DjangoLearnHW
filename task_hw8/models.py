from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager

from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "Category"
            db_table = "task_hw8_category"
            unique_together = ("name",)

status_choises = [
    ("New", "New"),
    ("In progress", "In progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done"),
    ("Archived", "Archived"),]



class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date='deadline')
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=40, choices=status_choises, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete = models.CASCADE,
       related_name = 'tasks',
       null = True,
       blank = True
    )
    class Meta:
        verbose_name = "Task"
        db_table = "task_hw8_task"
        ordering = ("-created_at",)
        unique_together = ("title",)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=status_choises)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'subtasks',
        null = True,
        blank = True
          )
    class Meta:
        verbose_name = "SubTask"
        db_table = "task_hw8_subtask"
        ordering = ("-created_at",)
        unique_together = ("title",)

    def __str__(self):
        return self.title
