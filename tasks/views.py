from os import write
from timeit import repeat
from urllib import response
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from django.db.models import Q
import csv


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'users/forms.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.request.session['update'] = 1
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'users/forms.html'

    def get_success_url(self):
        success_url = self.request.GET.get('next')
        self.request.session['update'] = 1
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
        self.request.session['update'] = 1
        return success_url


def checkTask(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = True
    task.save()
    request.session['update'] = 1
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def uncheckTask(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = False
    task.save()
    request.session['update'] = 1
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def exportReport(request):
    tasks = Task.objects.filter(owner=request.user)
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"Total number of tasks: {tasks.count()}"])
        
        writer.writerow(['Completed tasks'])
        tasks = Task.objects.filter(Q(owner=request.user) & Q(completed=True))
        writer.writerow(['ID', 'Title', 'Create at', 'Description'])
        for task in tasks:
            writer.writerow([task.pk, task.title, 
                            task.date_created.date().isoformat().replace('-','/'), 
                            task.description])

        writer.writerow(['On-going tasks'])
        tasks = Task.objects.filter(Q(owner=request.user) & Q(completed=False))
        writer.writerow(['ID', 'Title', 'Create at', 'Description'])
        for task in tasks:
            writer.writerow([task.pk, task.title, 
                            task.date_created.date().isoformat().replace('-','/'), 
                            task.description])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))