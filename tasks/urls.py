from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView, markTaskAsCompleted, unmarkTask


urlpatterns = [
    path('create-new-task',
        TaskCreateView.as_view(extra_context = {'label':'New Task', 'btn':'Create Task'}),
        name='create-task'),
    path('completed/<int:pk>',
        markTaskAsCompleted,
        name='mark-complete'),
    path('incompleted/<int:pk>',
        unmarkTask,
        name='unmark-complete'),
    path('edit-task/<int:pk>/<str:title>',
        TaskUpdateView.as_view(extra_context = {'form_type':'edit', 'label':'Edit Task', 'btn':'Edit'}),
        name='edit-task'),
    path('delete-task/<int:pk>/<str:title>',
        TaskDeleteView.as_view(),
        name='delete-task'),
    ]