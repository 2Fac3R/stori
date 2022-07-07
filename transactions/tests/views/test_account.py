"""Account views testing."""

# Python
import random

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# App
from ...models import Account, Transaction


class AccountListViewTest(TestCase):

    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_view_url_exists_at_desired_location(self):
        """Test view url exists at desired location."""
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test view url is accessible by name."""
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test view uses the correct template."""
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/list.html')

    def test_view_uses_correct_detail_template(self):
        """Test view uses the correct detail template."""
        self.account = Account.objects.create(id=100, user=self.user)
        self.number_of_transactions = 10
        for transaction_id in range(self.number_of_transactions):
            Transaction.objects.create(
                id=transaction_id, date=timezone.now(), transaction=float(random.uniform(-1000, 1000)), account=self.account)
        response = self.client.get(
            reverse('account-detail', args=(self.account.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/detail.html')

    def test_view_list_is_empty(self):
        """Test view list is empty"""
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['account_list']), 0)

    def test_view_lists_all_accounts(self):
        """Test list of all accounts."""
        self.number_of_accounts = 3
        for account_id in range(self.number_of_accounts):
            """Create 3 accounts."""
            Account.objects.create(id=account_id, user=self.user)
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['account_list']), self.number_of_accounts)
