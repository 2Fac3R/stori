"""Admin Panel Config."""

# Python
import datetime
from operator import countOf

# Django
from django.contrib import admin, messages
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# App
from .models import Account, Transaction
from .filters import MonthFilter
from .forms import CsvImportForm


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('send-email/', self.send_email)]
        return new_urls + urls

    def send_email(self, request):
        account = Account.objects.filter(user=request.user)
        operations = Transaction.objects.filter(
            account=account[0:1]).values_list('transaction', flat=True)
        months = Transaction.objects.filter(
            account=account[0:1]).values_list('date__month', flat=True)

        months_of_year = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        number_month_tuple = [(x, m)
                              for x, m in zip(range(1, 13), months_of_year)]
        credit = sum([float(x) for x in operations if float(x) > 0] or None)
        debit = sum([float(x) for x in operations if float(x) < 0] or None)
        credit_operations = [float(x)
                             for x in operations if float(x) > 0] or None
        debit_operations = [float(x)
                            for x in operations if float(x) < 0] or None
        total_balance = sum([float(x) for x in operations] or None)
        average_credit = credit/len(credit_operations)
        average_debit = debit/len(debit_operations)
        number_transactions_each_month = [[number_month_tuple[x-1], countOf(months, x)]
                                          for x in range(1, 13)] or None

        msg_html = render_to_string(
            'email/account_info.html',
            {
                'account': account.first,
                'total_balance': total_balance,
                'average_credit': average_credit,
                'average_debit': average_debit,
                'number_transactions_each_month': number_transactions_each_month
            })
        if request.method == "GET":
            try:
                send_mail(
                    'Stori: Account summary info', 'Account info',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    html_message=msg_html)
                self.message_user(request, "Email succesfully sent!")
            except Exception as error:
                messages.warning(request, error)
            url = reverse('admin:transactions_account_changelist')
            return HttpResponseRedirect(url)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'transaction', 'account')
    list_filter = (MonthFilter, 'account')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            current_account = Account.objects.get(user=request.user)

            for row in csv_data:
                try:
                    fields = row.split(",")
                    created = Transaction.objects.update_or_create(
                        id=fields[0],
                        defaults={
                            'date': datetime.datetime.strptime(fields[1], "%m/%d").date(),
                            'transaction': fields[2],
                            'account': current_account
                        }
                    )
                except IndexError:
                    """Ignore -> IndexError: list index out of range."""
                    continue
                except ValueError as error:
                    messages.warning(request, error)
                    return HttpResponseRedirect(request.path_info)
            self.message_user(request, "File succesfully uploaded!")
            url = reverse('admin:transactions_transaction_changelist')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
