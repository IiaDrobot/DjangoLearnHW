from django.apps import AppConfig


class TaskHw8Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_hw8'

    def ready(self):
        import task_hw8.signals




