from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Category, Task


User = get_user_model()


class RegisterAPITestCase(APITestCase):
    def test_user_can_register(self):
        payload = {
            'username': 'charlie',
            'password': '12345678',
        }

        response = self.client.post(reverse('register'), payload, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username = 'charlie').exists())

    def test_user_cannot_register_same_username_twice(self):
        User.objects.create_user(username = 'charlie', password = '12345678')

        payload = {
            'username': 'charlie',
            'password': '87654321',
        }

        response = self.client.post(reverse('register'), payload, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username = 'alice', password = '123456')
        self.user2 = User.objects.create_user(username = 'bob', password = '123456')

        self.category1 = Category.objects.create(name = 'Work', owner = self.user1)
        self.category2 = Category.objects.create(name = 'Personal', owner = self.user2)

    def test_user_sees_only_own_categories(self):
        self.client.force_authenticate(user = self.user1)

        response = self.client.get(reverse('category_list_create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Work')

    def test_user_cannot_access_other_users_category(self):
        self.client.force_authenticate(user = self.user1)

        response = self.client.get(reverse('category_detail', kwargs = {'pk': self.category2.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username = 'alice',
            password = '123456'
        )
        self.user2 = User.objects.create_user(
            username = 'bob',
            password = '123456'
        )

        self.task1 = Task.objects.create(
            title = 'Task 1',
            description = 'First task',
            status = 'todo',
            owner = self.user1,
        )
        self.task2 = Task.objects.create(
            title = 'Task 2',
            description = 'Second task',
            status = 'in_progress',
            owner = self.user2,
        )

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(user = self.user1)

        response = self.client.get(reverse('task_list_create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')

    def test_user_cannot_access_other_users_task(self):
        self.client.force_authenticate(user = self.user1)

        url = reverse('task_detail', kwargs = {'pk': self.task2.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_task(self):
        self.client.force_authenticate(user = self.user1)

        payload = {
            'title': 'New task',
            'description': 'Created by Alice',
            'status': 'todo',
        }

        response = self.client.post(
            reverse('task_list_create'),
            payload,
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New task')
        self.assertEqual(response.data['owner'], self.user1.id)

    def test_user_can_update_own_task(self):
        self.client.force_authenticate(user = self.user1)

        payload = {
            'title': 'Updated task',
            'status': 'done',
        }

        response = self.client.patch(
            reverse('task_detail', kwargs = {'pk': self.task1.pk}),
            payload,
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated task')
        self.assertEqual(self.task1.status, 'done')

    def test_user_can_delete_own_task(self):
        self.client.force_authenticate(user = self.user1)

        response = self.client.delete(
            reverse('task_detail', kwargs = {'pk': self.task1.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk = self.task1.pk).exists())