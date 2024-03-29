from datetime import datetime
from uuid import UUID

from django.http import JsonResponse
from ninja import NinjaAPI, Schema
from typing import List
from btc_wallet.models.models import Transaction
from btc_wallet.services.transferservice import TransferService
from decimal import Decimal

api = NinjaAPI()


class TransactionOut(Schema):
    # Schema for data types
    transaction_id: UUID
    amount: Decimal
    spent: bool
    created_at: datetime


class Config:
    # Format UUID and datetime to json format
    json_encoders = {
        UUID: lambda v: str(v),
        datetime: lambda v: v.isoformat(),
    }


class BalanceOut(Schema):
    balance_btc: Decimal
    balance_eur: Decimal


class TransferIn(Schema):
    amount_eur: Decimal

class AddBalanceIn(Schema):
    amount_eur: Decimal


@api.get("/transactions", response=List[TransactionOut])
def list_transactions(request):
    # List all transactions
    transactions = Transaction.objects.all()
    return transactions


@api.get("/balance", response=BalanceOut)
def show_balance(request):
    # Show balance in btc and eur
    unspent_transactions = Transaction.objects.filter(spent=False)
    balance_btc = sum(tx.amount for tx in unspent_transactions)
    exchange_rate = TransferService.get_btc_exchange_rate()
    balance_eur = balance_btc * exchange_rate
    return {'balance_btc': balance_btc, 'balance_eur': balance_eur}


@api.post("/transfer", response={201: None})
def create_transfer(request, data: TransferIn):
    # Create a new transfer
    try:
        TransferService.create_transfer(data.amount_eur)
        return 201, "Transfer created successfully."
    except ValueError as e:
        return 400, str(e)


@api.post("/add", response={201: None})
def add_balance_eur(request, data: AddBalanceIn):
    # Add more balance to wallet
    try:
        TransferService.add_balance(data.amount_eur)
        return JsonResponse({"message": "Funds added successfully in BTC."}, status=201)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
