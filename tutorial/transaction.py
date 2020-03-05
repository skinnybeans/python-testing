import time

from math import trunc


def process_transaction(account_id, amount):
    transaction_time = time.time()
    amount = trunc(amount)

    print(f'Performed transaction at time: {transaction_time} for amount: {amount}')
