from django.urls import path
from .views import TaskListView
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view() , name='home-page')
]