from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'users/forms.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'users/forms.html'

    def get_success_url(self):
        success_url = self.request.GET.get('next')
        return success_url

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.owner:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.owner:
            return True
        return False

    def get_success_url(self):
        success_url = self.request.GET.get('next')
        return success_url


def markTaskAsCompleted(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = True
    task.save()
    # return redirect('home-page')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def unmarkTask(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = False
    task.save()
    # return redirect('user-profile')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))