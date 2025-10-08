# /examples/6_implementation_pitfalls/6_3_non_reentrant_lock_deadlock/bad_example.py

import threading

# A standard, non-reentrant lock.
# It cannot be acquired more than once by the same thread.
lock = threading.Lock()

def helper_function():
    """A helper that also needs to acquire the lock."""
    print(f"[{threading.current_thread().name}] Helper trying to acquire the same lock...")
    
    # --- The Deadlock is Here ---
    # This thread already holds 'lock' from the main_function.
    # Since threading.Lock is non-reentrant, this call will block forever,
    # waiting for a lock that this very thread is holding.
    lock.acquire()
    
    print(f"[{threading.current_thread().name}] Helper acquired lock (this will never be printed).")
    lock.release()

def main_function():
    """The main function that acquires the lock first."""
    print(f"[{threading.current_thread().name}] Main function acquiring lock...")
    lock.acquire()
    
    print(f"[{threading.current_thread().name}] Main function acquired lock.")
    
    # Now, call the helper function, which will attempt to acquire the same lock.
    helper_function()
    
    lock.release()
    print(f"[{threading.current_thread().name}] Main function released lock (this will never be printed).")


if __name__ == "__main__":
    print("--- Non-Reentrant Lock Deadlock Demonstration ---")
    
    worker_thread = threading.Thread(target=main_function, name="Worker")
    worker_thread.start()
    
    # Use a timeout on join to demonstrate that the thread is stuck.
    worker_thread.join(timeout=3)
    
    if worker_thread.is_alive():
        print("\nDEADLOCK DETECTED: The worker thread is stuck.")
        print("It's waiting for a lock that it already owns.")
    else:
        print("\nThread finished (this should not happen).")