from re import search

from django.contrib import admin
from task_hw8.models import Task, SubTask, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','deadline','status')
    list_filter = ('title','deadline','status','categories')
    search_fields = ('title','description')
    list_per_page = 6

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','description','deadline','status','task','created_at')
    list_filter = ('task','deadline','status')
    search_fields = ('title','description')
    list_per_page = 6

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



#admin.site.register(Task)
#admin.site.register(SubTask)
#admin.site.register(Category)



# Register your models here.
