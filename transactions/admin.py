"""Admin Panel Config."""

# Python


# Django
from django.contrib import admin

# App
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    
        
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'transaction', 'account')
