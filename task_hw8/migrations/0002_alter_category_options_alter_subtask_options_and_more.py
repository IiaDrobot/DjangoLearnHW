# Generated by Django 5.2 on 2025-04-08 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_hw8', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='subtask',
            options={'ordering': ('-created_at',), 'verbose_name': 'SubTask'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('-created_at',), 'verbose_name': 'Task'},
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='subtask',
            unique_together={('title',)},
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('title',)},
        ),
        migrations.AlterModelTable(
            name='category',
            table='task_hw8_category',
        ),
        migrations.AlterModelTable(
            name='subtask',
            table='task_hw8_subtask',
        ),
        migrations.AlterModelTable(
            name='task',
            table='task_hw8_task',
        ),
    ]
