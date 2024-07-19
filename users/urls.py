from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.register , name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='users/forms.html', 
        redirect_authenticated_user=True, 
        extra_context={'label': 'Login Form', 'btn': 'Sign In','form_type':'login'}), 
        name='login'),

    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', http_method_names=["get"]) , name='logout'),
    path('logout/', views.LogoutUser , name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/forms.html',
        extra_context={'label': 'Password Reset','btn': 'Submit Request', 
        'description':'Please enter your E-mail to send you a password reset link'}), 
        name='password-reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/forms.html',
        extra_context={'label': 'Password Reset Form','btn': 'Confirm Reset',
        'description':'Plaese enter your new password'}), 
        name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),

    path('profile/', views.user_profile , name='user-profile'),

    path('profile-update/', views.user_profile_update , name='update-profile'),


    path('delete-user/<int:pk>/<str:title>',
        views.UserDeleteView.as_view(),
        name='delete-user'),
]