from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Task
from .permissions import IsOwner
from .serializers import CategorySerializer, TaskSerializer, UserRegisterSerializer


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response(
            {
                'username': user.username,
                'message': 'User created successfully',
            },
            status = status.HTTP_201_CREATED,
        )


class TaskFilter(filters.FilterSet):
    deadline = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['status', 'deadline']


class TaskListCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline']

    def get_queryset(self):
        return Task.objects.filter(owner = self.request.user)

    def get(self, request):
        tasks = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(tasks)

        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tasks, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        task = serializer.save(owner = request.user)
        return Response(
            self.get_serializer(task).data,
            status = status.HTTP_201_CREATED,
        )


class TaskDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self, request, pk):
        task = get_object_or_404(Task, pk = pk)
        self.check_object_permissions(request, task)
        return task

    def get(self, request, pk):
        task = self.get_object(request, pk)
        return Response(self.get_serializer(task).data)

    def patch(self, request, pk):
        task = self.get_object(request, pk)
        serializer = self.get_serializer(task, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        task = self.get_object(request, pk)
        task.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner = self.request.user)

    def get(self, request):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        category = serializer.save(owner = request.user)
        return Response(
            self.get_serializer(category).data,
            status = status.HTTP_201_CREATED,
        )


class CategoryDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self, request, pk):
        category = get_object_or_404(Category, pk = pk)
        self.check_object_permissions(request, category)
        return category

    def get(self, request, pk):
        category = self.get_object(request, pk)
        return Response(self.get_serializer(category).data)

    def patch(self, request, pk):
        category = self.get_object(request, pk)
        serializer = self.get_serializer(category, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_object(request, pk)
        category.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

