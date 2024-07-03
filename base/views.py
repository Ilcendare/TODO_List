from django.shortcuts import render
from tasks.models import Task
from django.views.generic import ListView


# *function based view
# def home_page(request):
#     tasks = Task.objects.filter(owner=request.user)
#     context = {'tasks':tasks}
#     return render(request, 'base/home.html', context)


# *class based view
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/home.html'
    ordering = ['date_created']
    paginate_by = 10