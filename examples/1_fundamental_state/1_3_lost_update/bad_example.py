# /examples/1_fundamental_state/1_3_lost_update/bad_example.py

import threading
import time

class BankAccount:
    """
    A simple, non-thread-safe bank account.
    This class is vulnerable to the "lost update" problem.
    """
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance

    def deposit(self, amount):
        """
        Deposits an amount into the account. This operation is not atomic.
        """
        # 1. Read the current balance
        current_balance = self.balance
        # Simulate some processing time or network latency
        time.sleep(0.0001)
        # 2. Modify the balance
        new_balance = current_balance + amount
        # 3. Write the new balance back
        self.balance = new_balance
        # print(f"Deposited {amount}, new balance is {self.balance}")

    def withdraw(self, amount):
        """
        Withdraws an amount from the account. This is also not atomic.
        """
        # 1. Read the current balance
        current_balance = self.balance
        # Simulate work
        time.sleep(0.0001)
        # 2. Modify the balance
        new_balance = current_balance - amount
        # 3. Write the new balance back
        self.balance = new_balance
        # print(f"Withdrew {amount}, new balance is {self.balance}")


def run_transactions(account, num_transactions):
    """A worker function for threads to perform deposits and withdrawals."""
    for _ in range(num_transactions):
        account.deposit(10)
        account.withdraw(10)


if __name__ == "__main__":
    NUM_THREADS = 20
    TRANSACTIONS_PER_THREAD = 100
    INITIAL_BALANCE = 1000

    account = BankAccount(INITIAL_BALANCE)
    
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=run_transactions, args=(account, TRANSACTIONS_PER_THREAD))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("--- Lost Update Example ---")
    print(f"Initial balance: {INITIAL_BALANCE}")
    print(f"Final balance:   {account.balance}")
    print(f"Difference:      {INITIAL_BALANCE - account.balance}")
    print("\nBecause deposits and withdrawals are not atomic, some transactions were 'lost',")
    print("resulting in an incorrect final balance.")