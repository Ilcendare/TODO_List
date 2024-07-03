from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView


urlpatterns = [
    path('create-new-task',
        TaskCreateView.as_view(extra_context = {'label':'New Task', 'btn':'Create Task'}),
        name='create-task'),
    path('edit-task/<int:pk>/<str:title>',
        TaskUpdateView.as_view(extra_context = {'label':'Edit Task', 'btn':'Edit'}),
        name='edit-task'),
    path('delete-task/<int:pk>/<str:title>',
        TaskDeleteView.as_view(),
        name='delete-task'),
    ]