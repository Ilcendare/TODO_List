from django.shortcuts import render
from tasks.models import Task
from django.views.generic import ListView
from django.db.models import Q

#* Function Based View
# def home_page(request):
#     tasks = Task.objects.filter(owner=request.user)
#     context = {'tasks':tasks}
#     return render(request, 'base/home.html', context)


#* Class Based View
class TaskListView(ListView):
    model = Task
    template_name = 'base/home.html'
    ordering = ['date_created']
    paginate_by = 10

    #* To get/filter all specific user's tasks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['tasks'] = None
            return context
        query = self.request.GET.get('query') if self.request.GET.get('query') is not None else ''
        tasks = Task.objects.filter(Q(owner=self.request.user) & 
                                    Q(completed=False) & 
                                    Q(title__icontains = query))
        context['tasks'] = tasks
        return context