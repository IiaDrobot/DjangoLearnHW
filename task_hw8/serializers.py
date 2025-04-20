from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']





class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']



def validate_name(value):
    if Category.objects.filter(name=value).exists():
        raise serializers.ValidationError("Категория с таким названием уже существует.")
    return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data and Category.objects.exclude(id=instance.id).filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return super().update(instance, validated_data)



class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(source='subtask_set', many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']



def validate_deadline(value):
    if value < timezone.now():
        raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
    return value


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


