from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView, checkTask, uncheckTask, exportReport


urlpatterns = [
    path('create-new-task',
        TaskCreateView.as_view(extra_context = {'label':'New Task', 'btn':'Create Task'}),
        name='create-task'),

    path('completed/<int:pk>',
        checkTask,
        name='mark-complete'),

    path('incompleted/<int:pk>',
        uncheckTask,
        name='unmark-complete'),

    path('edit-task/<int:pk>/<str:title>',
        TaskUpdateView.as_view(extra_context = {'form_type':'edit', 'label':'Edit Task', 'btn':'Edit'}),
        name='edit-task'),

    path('delete-task/<int:pk>/<str:title>',
        TaskDeleteView.as_view(),
        name='delete-task'),

    path('export-report/', exportReport ,name='export'),
    ]