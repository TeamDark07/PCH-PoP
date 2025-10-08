# /examples/3_resource_contention/3_1_deadlock/bad_example.py

import threading
import time

# Create two locks (our shared resources)
lock_a = threading.Lock()
lock_b = threading.Lock()

def worker_one():
    """
    This worker acquires Lock A, then tries to acquire Lock B.
    """

    print("[Worker 1] Attempting to acquire Lock A...")
    lock_a.acquire()
    print("[Worker 1] Acquired Lock A.")

    # A small sleep to ensure Worker 2 has time to acquire Lock B
    time.sleep(1)

    print("[Worker 1] Attempting to acquire Lock B...")
    # --- This is where Worker 1 will block ---
    lock_b.acquire()
    print("[Worker 1] Acquired Lock B.")

    # Release locks
    lock_b.release()
    lock_a.release()
    print("[Worker 1] Finished.")


def worker_two():
    """
    This worker acquires Lock B, then tries to acquire Lock A.
    This difference in acquisition order is the cause of the deadlock.
    """
    print("[Worker 2] Attempting to acquire Lock B...")
    lock_b.acquire()
    print("[Worker 2] Acquired Lock B.")

    # A small sleep to ensure Worker 1 has time to acquire Lock A
    time.sleep(1)

    print("[Worker 2] Attempting to acquire Lock A...")
    # --- This is where Worker 2 will block ---
    lock_a.acquire()
    print("[Worker 2] Acquired Lock A.")

    # Release locks
    lock_a.release()
    lock_b.release()
    print("[Worker 2] Finished.")


if __name__ == "__main__":
    print("--- Deadlock Example ---")
    
    thread1 = threading.Thread(target=worker_one)
    thread2 = threading.Thread(target=worker_two)

    thread1.start()
    thread2.start()

    print("[Main] Waiting for threads to finish...")
    
    # The .join() calls will block forever because the threads are deadlocked.
    thread1.join(timeout=5)
    thread2.join(timeout=5)
    
    if thread1.is_alive() or thread2.is_alive():
        print("\nDEADLOCK DETECTED! The threads are stuck and will not finish.")
    else:
        print("\nThreads finished (this should not happen).")