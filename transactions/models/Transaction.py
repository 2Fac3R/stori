"""Transaction model."""

# Django
from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns

# App
from .Account import Account


class Transaction(models.Model):
    date = models.DateField()
    transaction = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.transaction)
    
    def get_absolute_url(self):
        """Returns the url to access a particular product instance."""
        return reverse('transaction-detail', args=[str(self.id)])
