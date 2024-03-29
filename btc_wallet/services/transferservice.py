import requests
from decimal import Decimal, ROUND_DOWN

from ninja.errors import HttpError
from requests import Response

from btc_wallet.models.models import Transaction


class TransferService:
    # Methods for transfer service
    MIN_TRANSFER_AMOUNT_BTC = Decimal('0.00001')
    BTC_EUR_URL = "http://api-cryptopia.adca.sh/v1/prices/ticker"

    @staticmethod
    def get_btc_exchange_rate():
        # Exchange rate method
        response = requests.get(TransferService.BTC_EUR_URL)
        data = response.json()
        # Filter out the BTC/EUR rate from the response
        btc_eur_rate = next(item for item in data['data'] if item['symbol'] == 'BTC/EUR')['value']
        return Decimal(btc_eur_rate)

    @staticmethod
    def create_transfer(amount_eur):
        try:
            # Convert EUR to BTC
            exchange_rate = TransferService.get_btc_exchange_rate()
            amount_btc = (Decimal(amount_eur) / exchange_rate).quantize(Decimal('.00001'), rounding=ROUND_DOWN)
            if amount_btc < TransferService.MIN_TRANSFER_AMOUNT_BTC:
                raise ValueError("Transfer amount is too small.")
            # Fetch unspent transactions
            unspent_transactions = Transaction.objects.filter(spent=False).order_by('created_at')
            # Calculate total unspent amount
            total_unspent = sum(tx.amount for tx in unspent_transactions)
            if total_unspent < amount_btc:
                raise ValueError("Insufficient funds.")
            # Process transactions to cover the transfer amount
            spent_amount = Decimal('0')
            for tx in unspent_transactions:
                if spent_amount < amount_btc:
                    tx.spent = True
                    tx.save()
                    spent_amount += tx.amount
                else:
                    break
            # Create a new unspent transaction for the leftover amount
            if spent_amount > amount_btc:
                leftover_amount = spent_amount - amount_btc
                Transaction.objects.create(amount=leftover_amount, spent=False)
            # Return if successful
            return "Transfer successful."
        except ValueError as e:
            raise HttpError(400, str(e))

    @staticmethod
    def add_balance(amount_eur):
        # Add balance to wallet
        exchange_rate = TransferService.get_btc_exchange_rate()
        amount_btc = (Decimal(amount_eur) / exchange_rate).quantize(Decimal('.00001'), rounding=ROUND_DOWN)
        if amount_btc < TransferService.MIN_TRANSFER_AMOUNT_BTC:
            raise ValueError("The amount to add is too small.")
        Transaction.objects.create(amount=amount_btc, spent=False)
        return "Funds added successfully."
