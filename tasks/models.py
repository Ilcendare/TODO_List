from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse("home-page")
    
