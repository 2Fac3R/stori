"""Account views."""

# Python
from operator import countOf

# Django
from django.views import generic

# App
from ..models import Account, Transaction


class AccountListView(generic.ListView):
    model = Account
    ordering = ['id']
    template_name = 'accounts/list.html'


class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'accounts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        operations = Transaction.objects.filter(
            account=self.get_object()).values_list('transaction', flat=True)
        months = Transaction.objects.filter(
            account=self.get_object()).values_list('date__month', flat=True)

        months_of_year = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        number_month_tuple = [(x, m)
                              for x, m in zip(range(1, 13), months_of_year)]

        number_transactions_each_month = [[number_month_tuple[x-1], countOf(months, x)]
                                          for x in range(1, 13)] or None

        credit = sum([float(x) for x in operations if float(x) > 0] or None)
        debit = sum([float(x) for x in operations if float(x) < 0] or None)
        credit_operations = [float(x)
                             for x in operations if float(x) > 0] or None
        debit_operations = [float(x)
                            for x in operations if float(x) < 0] or None
        total_balance = sum([float(x) for x in operations] or None)

        context['total_balance'] = total_balance
        context['average_credit'] = credit/len(credit_operations)
        context['average_debit'] = debit/len(debit_operations)
        context['number_transactions_each_month'] = number_transactions_each_month

        return context
