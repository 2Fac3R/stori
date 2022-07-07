"""Account model testing."""

# Django
from django.test import TestCase
from django.contrib.auth.models import User

# App
from ...models import Account


class AccountModelTest(TestCase):
    
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        Account.objects.create(id=1, user=self.user)

    def test_get_absolute_url(self):
        """Test absolute url for account-detail."""
        account = Account.objects.get(id=1)
        # This will fail if the urlconf is not defined.
        self.assertEquals(account.get_absolute_url(), '/accounts/1')
