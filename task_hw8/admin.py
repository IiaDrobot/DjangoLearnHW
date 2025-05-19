from re import search

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from task_hw8.models import Task, SubTask, Category


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.action(description="Архивировать задачи со статусом 'Done'")
def mark_as_archived(modeladmin, request, queryset):
    done_tasks = queryset.filter(status="Done")
    count = done_tasks.update(status="Archived")
    modeladmin.message_user(request, f"Архивировано задач: {count}", messages.SUCCESS)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'created_at', 'deadline', 'status')
    list_filter = ('title', 'deadline', 'status', 'categories')
    search_fields = ('title', 'description')
    list_per_page = 6
    inlines = [SubTaskInline]
    actions = [mark_as_archived]
    fields = ('title', 'description', 'deadline', 'status', 'categories', 'owner')

    def short_title(self, obj):
        short = obj.title[:10] + "..." if len(obj.title) > 10 else obj.title
        return format_html("<span title='{}'>{}</span>", obj.title, short)
    short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deadline', 'status', 'task', 'created_at')
    list_filter = ('task', 'deadline', 'status')
    search_fields = ('title', 'description')
    list_per_page = 6

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

#admin.site.register(Task)
#admin.site.register(SubTask)
#admin.site.register(Category)



# Register your models here.
