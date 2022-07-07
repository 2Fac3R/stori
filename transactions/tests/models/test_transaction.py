"""Transaction model testing."""

# Django
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

# App
from ...models import Transaction, Account


class TransactionModelTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.account = Account.objects.create(id=1, user=self.user)
        Transaction.objects.create(
            id=1, date=timezone.now(), transaction=26.15, account=self.account)

    def test_get_absolute_url(self):
        """Test absolute url for transaction-detail."""
        transaction = Transaction.objects.get(id=1)
        # This will fail if the urlconf is not defined.
        self.assertEquals(transaction.get_absolute_url(), '/transactions/1')
