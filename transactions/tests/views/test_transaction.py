"""Transaction views testing."""

# Python
import random

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# App
from ...models import Transaction, Account


class TransactionListViewTest(TestCase):

    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_view_url_exists_at_desired_location(self):
        """Test view url exists at desired location."""
        response = self.client.get('/transactions/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view url is accessible by name."""
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/list.html')

    def test_view_uses_correct_detail_template(self):
        """Test view uses the correct detail template."""
        self.account = Account.objects.create(id=1, user=self.user)
        self.transaction = Transaction.objects.create(
            id=1, date=timezone.now(), transaction=float(random.uniform(-1000, 1000)), account=self.account)
        response = self.client.get(
            reverse('transaction-detail', args=(self.transaction.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/detail.html')

    def test_view_list_is_empty(self):
        """Test view list is empty"""
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transaction_list']), 0)

    def test_lists_all_transactions(self):
        """Test list of all Transactions."""
        self.account = Account.objects.create(id=1, user=self.user)
        self.number_of_transactions = 10
        for transaction_id in range(self.number_of_transactions):
            """Create 10 transactions."""
            Transaction.objects.create(
                id=transaction_id, date=timezone.now(), transaction=26.15, account=self.account)
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['transaction_list']), self.number_of_transactions)
