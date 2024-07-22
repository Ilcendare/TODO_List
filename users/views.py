from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'The user {username} has been created successfuly')
            return redirect('login')
    else:
        form = UserRegisterationForm()
    context = {'form': form, 'label': 'Register Form', 'btn': 'Sign Up','form_type':'register',
                'description':'Please fill in the form to creat a new account.'}
    return render(request, 'users/forms.html', context)


def LogoutUser(request):
    logout(request)
    return render(request, 'users/logout.html')


def user_profile(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-completed')
    paginated = Paginator(tasks, 10)
    page_number = request.GET.get('page') #Get the requested page number from the URL
    page = paginated.get_page(page_number)
    context = {'tasks': page, 'is_paginated': True}
    return render(request, 'users/profile.html', context)


def user_profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'The profile has been updated successfuly')
            return redirect('user-profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
    context = {'u_form':user_form, 'p_form': profile_form}
    return render(request, 'users/profile_update.html', context)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False