# /examples/3_resource_contention/3_1_deadlock/good_example.py

import threading
import time

# Create two locks
lock_a = threading.Lock()
lock_b = threading.Lock()

# --- The Solution: A Lock Ordering Policy ---
# We define a strict, global order in which locks must be acquired.
# In this case, Lock A must always be acquired before Lock B.
# This prevents the circular dependency that causes deadlocks.

def worker_one():
    """
    This worker acquires locks in the correct order: A then B.
    """
    print("[Worker 1] Running...")
    
    with lock_a:
        print("[Worker 1] Acquired Lock A.")
        time.sleep(1)
        
        print("[Worker 1] Attempting to acquire Lock B...")
        with lock_b:
            print("[Worker 1] Acquired Lock B.")
            # Do work with both resources
            print("[Worker 1] Doing work with both locks.")

    print("[Worker 1] Finished and released locks.")


def worker_two():
    """
    This worker also acquires locks in the correct order: A then B.
    Even though it "needs" Lock B first, it must follow the policy.
    """
    print("[Worker 2] Running...")
    
    with lock_a:
        print("[Worker 2] Acquired Lock A.")
        time.sleep(1)
        
        print("[Worker 2] Attempting to acquire Lock B...")
        with lock_b:
            print("[Worker 2] Acquired Lock B.")
            # Do work with both resources
            print("[Worker 2] Doing work with both locks.")

    print("[Worker 2] Finished and released locks.")


if __name__ == "__main__":
    print("--- Deadlock Avoidance Example ---")
    
    thread1 = threading.Thread(target=worker_one)
    thread2 = threading.Thread(target=worker_two)

    thread1.start()
    thread2.start()

    print("[Main] Waiting for threads to finish...")
    
    thread1.join()
    thread2.join()
    
    print("\nAll threads finished successfully. Deadlock was avoided.")