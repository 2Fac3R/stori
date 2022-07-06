"""Account views."""

# Django
from django.views import generic

# App
from ..models.Account import Account


class AccountListView(generic.ListView):
    model = Account
    ordering = ['id']
    template_name = 'accounts/account_list.html'
    

class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    