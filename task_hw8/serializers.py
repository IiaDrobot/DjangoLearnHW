from rest_framework import serializers
from django.utils import timezone
from task_hw8.models import Task,SubTask,Category
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 're_password', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"re_password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']



class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        #read_only_fields = ['created_at']
        read_only_fields = ['owner', 'created_at']

        def create(self, validated_data):
            return SubTask.objects.create(owner=self.context['request'].user, **validated_data)

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        owner = serializers.StringRelatedField(read_only=True)


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
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner','subtasks']



def validate_deadline(value):
    if value < timezone.now():
        raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
    return value


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']
    def create(self, validated_data):
        return Task.objects.create(owner=self.context['request'].user, **validated_data)

