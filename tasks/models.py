from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 50)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'categories')

    def __str__(self):
        return self.name

class Task(models.Model):
    CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    status = models.CharField(max_length = 20, choices = CHOICES, default = 'todo')
    deadline = models.DateTimeField(null = True, blank = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'tasks')
    categories = models.ManyToManyField(Category, blank = True, related_name = 'tasks')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title