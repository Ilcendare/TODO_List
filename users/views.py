from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UserRegisterationForm
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task

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
    tasks = Task.objects.filter(owner=request.user)
    context = {'tasks': tasks}
    return render(request, 'users/profile.html', context)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False