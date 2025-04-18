from django.db import models

status_choises = [
    ("New", "New"),
    ("In progress", "In progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done"),
    ("Archived", "Archived"),]

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        db_table = "task_hw8_category"
        unique_together = ("name",)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date='deadline')
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=40, choices=status_choises, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

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

    class Meta:
        verbose_name = "SubTask"
        db_table = "task_hw8_subtask"
        ordering = ("-created_at",)
        unique_together = ("title",)

    def __str__(self):
        return self.title
