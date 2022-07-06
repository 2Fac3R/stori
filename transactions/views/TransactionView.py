"""Transaction views."""

# Django
from django.views import generic

# App
from ..models.Transaction import Transaction


class TransactionListView(generic.ListView):
    model = Transaction
    ordering = ['date']


class TransactionDetailView(generic.DetailView):
    model = Transaction
