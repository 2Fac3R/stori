"""Admin Panel Config."""

# Python
import datetime

# Django
from django.contrib import admin, messages
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# App
from .models import Account, Transaction
from .filters import MonthFilter
from .forms import CsvImportForm


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    
        
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'transaction', 'account')
    list_filter = (MonthFilter, 'account')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
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
                        id = fields[0],
                        defaults = { 
                            'date' : datetime.datetime.strptime(fields[1], "%m/%d").date(),
                            'transaction' : fields[2],
                            'account' : current_account
                        }
                    )
                except IndexError:
                    """Ignore -> IndexError: list index out of range."""
                    continue
                except ValueError as error:
                    messages.warning(request, error)
                    return HttpResponseRedirect(request.path_info)
            url = reverse('admin:transactions_transaction_changelist')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)