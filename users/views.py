from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UserRegisterationForm
from django.contrib import messages


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
    return render(request, 'users/profile.html')