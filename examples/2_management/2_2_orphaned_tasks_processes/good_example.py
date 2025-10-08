# /examples/2_management/2_2_orphaned_tasks_processes/good_example.py

import threading
import time
import os

FILENAME = "managed_output.txt"

def slow_worker():
    """
    A worker that simulates a slow but important task.
    """
    print("[Worker] Starting task...")
    time.sleep(2)
    
    with open(FILENAME, 'w') as f:
        f.write("Important work complete.")
        
    print("[Worker] Task finished.")


if __name__ == "__main__":
    # Clean up file from previous runs
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

    print("[Main] Starting a worker thread and managing its lifecycle...")
    
    # --- Proper Management ---
    # 1. Store the thread object in a variable.
    worker_thread = threading.Thread(target=slow_worker)
    worker_thread.start()
    
    print("[Main] Main thread is now waiting for the worker to complete...")
    
    # 2. Call .join() on the thread object.
    # This blocks the main thread, preventing it from exiting until the
    # worker thread has finished its execution.
    worker_thread.join()
    
    print("[Main] Worker has finished. Main thread can now exit safely.")

    # Verification
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            content = f.read()
        print(f"\nVerification: File content is '{content}'")