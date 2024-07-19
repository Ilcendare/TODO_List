from django.shortcuts import render
from tasks.models import Task
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.core.serializers.json import DjangoJSONEncoder
import json

#* Function Based View
# def home_page(request):
#     tasks = Task.objects.filter(owner=request.user)
#     context = {'tasks':tasks}
#     return render(request, 'base/home.html', context)


#* Class Based View
class TaskListView(ListView):
    model = Task
    template_name = 'base/home.html'

    #* To get/filter all specific user's tasks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['tasks'] = None
            return context
        
        query = self.request.GET.get('query') if self.request.GET.get('query') is not None else ''
        task_order = int(self.request.GET.get('task-order')) if self.request.GET.get('task-order') is not None else 0
        
        if query != '' or task_order > 0:
            tasks = Task.objects.filter(Q(owner=self.request.user) & Q(title__icontains = query))
            
            if task_order == 1:
                tasks = tasks.order_by('-date_created')
            elif task_order == 2:
                tasks = tasks.order_by('date_created')
            elif task_order == 3:
                tasks = tasks.order_by(Lower('title'))
            else:
                tasks.order_by('completed','-date_created')

            self.request.session['query'] = query
            self.request.session['tasks'] = json.dumps(list(tasks.values()), cls=DjangoJSONEncoder)
        
        elif 'tasks' in self.request.session:
            tasks = json.loads(self.request.session.get('tasks'))
            
        else:
            tasks = Task.objects.filter(Q(owner=self.request.user))
            tasks.order_by('completed','-date_created')
            self.request.session['query'] = query
            self.request.session['tasks'] = json.dumps(list(tasks.values()), cls=DjangoJSONEncoder)

        paginated = Paginator(tasks, 10)
        page_number = self.request.GET.get('page') #Get the requested page number from the URL
        page = paginated.get_page(page_number)
        context['tasks'] = page
        context['is_paginated'] = True
        return context