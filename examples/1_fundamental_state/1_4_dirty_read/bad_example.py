# /examples/1_fundamental_state/1_4_dirty_read/bad_example.py

import threading
import time

class BankAccount:
    """A simple bank account class."""
    def __init__(self, balance=0):
        self.balance = balance

# Global flag to signal when the audit thread detects an issue.
dirty_read_detected = threading.Event()

def transfer(from_account, to_account, amount):
    """
    A multi-step transaction that is NOT atomic.
    It can be interrupted, leaving the system in an inconsistent state.
    """
    print("Transfer starting...")
    # Step 1: Debit from the first account
    from_account.balance -= amount
    
    # --- The Inconsistent Window ---
    # At this point, the money has left the first account but has not yet
    # arrived in the second. The total system balance is incorrect.
    # A short sleep simulates work and increases the chance of an audit
    # thread seeing this inconsistent state.
    time.sleep(0.01)
    
    # Step 2: Credit to the second account
    to_account.balance += amount
    print("Transfer complete.")

def audit(accounts, expected_total):
    """
    An auditor thread that continuously checks for system consistency.
    It runs until a dirty read is detected.
    """
    print("Auditor starting...")
    while not dirty_read_detected.is_set():
        current_total = sum(acc.balance for acc in accounts)
        if current_total != expected_total:
            print("\n--- DIRTY READ DETECTED! ---")
            print(f"Audit found total balance of {current_total}, expected {expected_total}.")
            print("This happened because the audit ran mid-transfer.")
            dirty_read_detected.set()
            break
        time.sleep(0.001)
    print("Auditor finished.")

if __name__ == "__main__":
    INITIAL_BALANCE = 1000
    TOTAL_MONEY = INITIAL_BALANCE * 2

    account1 = BankAccount(INITIAL_BALANCE)
    account2 = BankAccount(INITIAL_BALANCE)

    # The transfer thread will move money from account1 to account2
    transfer_thread = threading.Thread(target=transfer, args=(account1, account2, 500))
    
    # The audit thread will watch the accounts
    audit_thread = threading.Thread(target=audit, args=([account1, account2], TOTAL_MONEY))
    
    audit_thread.start()
    # A small delay to ensure the auditor is running before the transfer starts
    time.sleep(0.005)
    transfer_thread.start()

    transfer_thread.join()
    # Ensure the auditor stops if the transfer finishes without detection
    dirty_read_detected.set() 
    audit_thread.join()

    print("\n--- Final Account Balances ---")
    print(f"Account 1: {account1.balance}")
    print(f"Account 2: {account2.balance}")
    print(f"Final Total: {account1.balance + account2.balance}")