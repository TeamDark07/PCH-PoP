# /examples/6_implementation_pitfalls/6_3_non_reentrant_lock_deadlock/good_example.py

import threading

# --- The Solution: A Re-entrant Lock (RLock) ---
# An RLock can be acquired multiple times by the same thread.
# It maintains an ownership counter.
lock = threading.RLock()

def helper_function():
    """A helper that also needs to acquire the re-entrant lock."""
    print(f"[{threading.current_thread().name}] Helper trying to acquire the RLock...")
    
    # This call will succeed immediately because this thread already owns the lock.
    # The internal counter of the RLock is simply incremented.
    lock.acquire()
    
    print(f"[{threading.current_thread().name}] Helper acquired RLock successfully.")
    
    # This release decrements the counter. The lock is not fully released yet.
    lock.release()
    print(f"[{threading.current_thread().name}] Helper released RLock.")

def main_function():
    """The main function that acquires the RLock first."""
    print(f"[{threading.current_thread().name}] Main function acquiring RLock...")
    lock.acquire() # Ownership counter becomes 1
    
    print(f"[{threading.current_thread().name}] Main function acquired RLock.")
    
    # Call the helper function.
    helper_function()
    
    # This final release decrements the counter to 0, fully releasing the lock.
    lock.release()
    print(f"[{threading.current_thread().name}] Main function released RLock.")


if __name__ == "__main__":
    print("--- Re-entrant Lock (RLock) Solution ---")
    
    worker_thread = threading.Thread(target=main_function, name="Worker")
    worker_thread.start()
    
    worker_thread.join() # No timeout needed, the thread will finish.
    
    print("\nSUCCESS: The worker thread completed without deadlocking.")