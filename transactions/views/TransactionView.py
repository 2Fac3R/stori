"""Transaction views."""

# Django
from django.views import generic

# App
from ..models import Transaction


class TransactionListView(generic.ListView):
    model = Transaction
    ordering = ['date']
    template_name = 'transactions/list.html'


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'transactions/detail.html'
