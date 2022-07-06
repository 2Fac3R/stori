"""Transaction URLs Configuration."""

# Django
from django.urls import path

# App
from .views import TransactionView as transaction_views
from .views import AccountView as account_views


urlpatterns = [
    # Transactions
    path('transactions/', transaction_views.TransactionListView.as_view(),
         name='transaction'),
    path('transactions/<int:pk>', transaction_views.TransactionDetailView.as_view(),
         name='transaction-detail'),
    # Accounts
    path('accounts/', account_views.AccountListView.as_view(), name='account'),
    path('accounts/<int:pk>', account_views.AccountDetailView.as_view(),
         name='account-detail'),
]
