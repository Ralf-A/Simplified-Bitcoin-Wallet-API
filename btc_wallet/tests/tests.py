from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from django.test import TestCase
from btc_wallet.models import Transaction
from btc_wallet.services import TransferService

class TransactionAPITests(TestCase):
    def setUp(self):
        # Create test transactions
        self.transaction1 = Transaction.objects.create(
            transaction_id=uuid4(),
            amount=Decimal('3.0'),
            spent=False,
            created_at=datetime.now()
        )
        self.transaction2 = Transaction.objects.create(
            transaction_id=uuid4(),
            amount=Decimal('2.0'),
            spent=False,
            created_at=datetime.now()
        )

    def test_list_transactions(self):
        response = self.client.get("/api/transactions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        # Add more assertions here to validate the response content

    def test_show_balance(self):
        # Mock the exchange rate
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        response = self.client.get("/api/balance")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.json()['balance_btc']), Decimal('5.0'))
        self.assertEqual(Decimal(response.json()['balance_eur']), Decimal('5.0'))
        # Add more assertions here to validate the response content

    def test_create_transfer(self):
        # Mock the exchange rate and transfer creation
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        TransferService.create_transfer = lambda amount_eur: None
        response = self.client.post("/api/transfer", json={'amount_eur': Decimal('4.5')})
        self.assertEqual(response.status_code, 201)
        # Add more assertions here to validate the response content

    def test_add_balance_eur(self):
        # Mock balance addition
        TransferService.add_balance = lambda amount_eur: None
        response = self.client.post("/api/add", json={'amount_eur': Decimal('1.0')})
        self.assertEqual(response.status_code, 201)
        # Add more assertions here to validate the response content

    # Add more test methods as needed for edge cases and error handling
