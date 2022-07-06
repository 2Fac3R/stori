"""Account model."""

# Django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # To generate URLS by reversing URL patterns


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        """Returns the url to access a particular product instance."""
        return reverse('account-detail', args=[str(self.id)])
