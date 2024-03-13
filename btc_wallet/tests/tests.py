import json
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from django.test import TestCase
from btc_wallet.models import Transaction
from btc_wallet.services import TransferService

class TransactionAPITests(TestCase):
    def setUp(self):
        # Setup by creating two transactions
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
        # Test listing transactions
        response = self.client.get("/api/transactions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_show_balance(self):
        # Test showing correct balance
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        response = self.client.get("/api/balance")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.json()['balance_btc']), Decimal('5.0'))
        self.assertEqual(Decimal(response.json()['balance_eur']), Decimal('5.0'))

    def test_create_transfer(self):
        # Test creating transfer
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        TransferService.create_transfer = lambda amount_eur: None
        payload = {'amount_eur': str(Decimal('4.5'))}
        response = self.client.post("/api/transfer", data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201, response.content)

    def test_add_balance_eur(self):
        # Test adding balance
        TransferService.add_balance = lambda amount_eur: None
        payload = {'amount_eur': str(Decimal('1.0'))}
        response = self.client.post("/api/add", data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_404_error(self):
        # Test getting an nonexisting page
        response = self.client.get("/api/nonexistent")
        self.assertEqual(response.status_code, 404)
        expected_response = {"error": "Page not found", "documentation": "https://github.com/Ralf-A/Simplified-Bitcoin-Wallet-API"}
        self.assertEqual(response.json(), expected_response)

    def test_add_balance_eur_with_incorrect_payload(self):
        # Test add balance with incorrect payload format
        incorrect_payload = {'wrong_key': '1.0'}
        response = self.client.post("/api/add", data=json.dumps(incorrect_payload), content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'][0]['msg'], 'Field required')

    def test_add_balance_eur_with_empty_payload(self):
        # Test add balance with empty payload
        empty_payload = {}
        response = self.client.post("/api/add", data=json.dumps(empty_payload), content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'][0]['msg'], 'Field required')

    def test_create_transfer_with_incorrect_payload(self):
        # Test create transfer with incorrect payload format
        incorrect_payload = {'wrong_key': '4.5'}
        response = self.client.post("/api/transfer", data=json.dumps(incorrect_payload), content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'][0]['msg'], 'Field required')

    def test_create_transfer_with_empty_payload(self):
        # Test create transfer with empty payload
        empty_payload = {}
        response = self.client.post("/api/transfer", data=json.dumps(empty_payload), content_type='application/json')
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'][0]['msg'], 'Field required')

    def test_create_transfer_with_insufficient_funds(self):
        # Test create transfer with an amount larger than the wallet balance
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        TransferService.create_transfer = lambda amount_eur: None
        payload = {'amount_eur': '800000000.0'}  # Change to string value
        response = self.client.post("/api/transfer", data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'], 'Insufficient funds.')

    def test_create_transfer_with_amount_too_small(self):
        # Test create transfer with an amount smaller than the minimum transfer amount
        TransferService.get_btc_exchange_rate = lambda: Decimal('1.0')
        TransferService.create_transfer = lambda amount_eur: None
        payload = {'amount_eur': '0.5'}  # Change to string value
        response = self.client.post("/api/transfer", data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'], 'Transfer amount is too small.')

