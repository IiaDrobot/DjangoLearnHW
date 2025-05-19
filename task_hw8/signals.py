
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from task_hw8.models import Task

@receiver(pre_save, sender=Task)
def notify_task_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        previous = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return
    if previous.status != instance.status:
        user = instance.owner
        if user and user.email:
            subject = f"Изменение статуса задачи: {instance.title}"
            message = (
                f"Здравствуйте, {user.username}!\n\n"
                f"Статус вашей задачи \"{instance.title}\" изменён с "
                f"\"{previous.status}\" на \"{instance.status}\".\n"
            )
            send_mail(subject, message, 'admin@example.com', [user.email])
