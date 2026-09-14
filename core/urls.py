from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks.views import (
    CategoryDetailAPIView,
    CategoryListCreateAPIView,
    RegisterAPIView,
    TaskDetailAPIView,
    TaskListCreateAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name = 'schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name = 'schema'), name = 'swagger_ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name = 'schema'), name = 'redoc'),
    path('api/register/', RegisterAPIView.as_view(), name = 'register'),
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name = 'task_list_create'),
    path('api/tasks/<int:pk>/', TaskDetailAPIView.as_view(), name = 'task_detail'),
    path('api/categories/', CategoryListCreateAPIView.as_view(), name = 'category_list_create'),
    path('api/categories/<int:pk>/', CategoryDetailAPIView.as_view(), name = 'category_detail'),
]
