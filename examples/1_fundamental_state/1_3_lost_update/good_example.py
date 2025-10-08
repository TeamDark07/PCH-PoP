# /examples/1_fundamental_state/1_3_lost_update/good_example.py

import threading
import time

class BankAccount:
    """
    A thread-safe bank account using a lock to prevent lost updates.
    """
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        """
        Atomically deposits an amount using a lock.
        """
        # The 'with' statement ensures the lock is acquired before the
        # critical section and released after, even if errors occur.
        with self.lock:
            # This entire block is now atomic. No other thread can execute
            # a deposit or withdrawal until this block is complete.
            current_balance = self.balance
            time.sleep(0.0001)
            new_balance = current_balance + amount
            self.balance = new_balance

    def withdraw(self, amount):
        """
        Atomically withdraws an amount using the same lock.
        """
        with self.lock:
            current_balance = self.balance
            time.sleep(0.0001)
            new_balance = current_balance - amount
            self.balance = new_balance


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

    print("--- Thread-Safe Example with Lock ---")
    print(f"Initial balance: {INITIAL_BALANCE}")
    print(f"Final balance:   {account.balance}")
    print(f"Difference:      {INITIAL_BALANCE - account.balance}")
    print("\nBy using a lock to make each transaction atomic, the final balance is correct.")