from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Task

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError('Username already taken.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'owner', 'categories', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']