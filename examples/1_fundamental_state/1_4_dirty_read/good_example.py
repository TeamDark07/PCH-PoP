# /examples/1_fundamental_state/1_4_dirty_read/good_example.py

import threading
import time

class BankAccount:
    """A simple bank account class."""
    def __init__(self, balance=0):
        self.balance = balance

# A single, system-wide lock to protect all multi-step transactions.
transaction_lock = threading.Lock()
stop_audit_event = threading.Event()

def transfer(from_account, to_account, amount):
    """
    A multi-step transaction that IS atomic because it's protected by a lock.
    """
    print("Transfer starting...")
    # By acquiring the lock, we ensure that the entire block of code
    # executes without interruption from any other thread holding the same lock.
    with transaction_lock:
        # Step 1: Debit from the first account
        from_account.balance -= amount
        
        # --- The Inconsistent Window is now protected ---
        # The audit thread cannot acquire the lock and read the balances
        # until this 'with' block is completed.
        time.sleep(0.01)
        
        # Step 2: Credit to the second account
        to_account.balance += amount
    print("Transfer complete.")

def audit(accounts, expected_total):
    """
    The auditor thread now also uses the lock to ensure it reads a
    consistent snapshot of the system state.
    """
    print("Auditor starting...")
    while not stop_audit_event.is_set():
        with transaction_lock:
            # By acquiring the lock here, the auditor can be sure that
            # no transaction is currently in progress.
            current_total = sum(acc.balance for acc in accounts)
        
        if current_total != expected_total:
            # This block should now be unreachable.
            print("\n--- INCONSISTENCY DETECTED! THIS SHOULD NOT HAPPEN! ---")
            stop_audit_event.set()
            break
        time.sleep(0.001)
    print("Auditor finished without detecting any dirty reads.")

if __name__ == "__main__":
    INITIAL_BALANCE = 1000
    TOTAL_MONEY = INITIAL_BALANCE * 2

    account1 = BankAccount(INITIAL_BALANCE)
    account2 = BankAccount(INITIAL_BALANCE)

    transfer_thread = threading.Thread(target=transfer, args=(account1, account2, 500))
    audit_thread = threading.Thread(target=audit, args=([account1, account2], TOTAL_MONEY))
    
    audit_thread.start()
    time.sleep(0.005)
    transfer_thread.start()

    transfer_thread.join()
    stop_audit_event.set() # Signal the auditor to stop cleanly
    audit_thread.join()

    print("\n--- Final Account Balances ---")
    print(f"Account 1: {account1.balance}")
    print(f"Account 2: {account2.balance}")
    print(f"Final Total: {account1.balance + account2.balance}")