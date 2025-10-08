# /examples/2_management/2_2_orphaned_tasks_processes/bad_example.py

import threading
import time
import os

FILENAME = "orphan_output.txt"

def slow_worker():
    """
    A worker that simulates a slow but important task, like writing to a file.
    """
    print("[Worker] Starting task...")
    time.sleep(2) # Simulate a long-running operation
    
    # This is the critical work that might not happen
    with open(FILENAME, 'w') as f:
        f.write("Important work complete.")
        
    print("[Worker] Task finished.")


if __name__ == "__main__":
    # Clean up file from previous runs
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

    print("[Main] Starting a worker thread (fire-and-forget)...")
    
    # --- The Orphan is Created Here ---
    # We create and start the thread but do not store a reference to it
    # and, crucially, we do not call .join(). This is an "orphaned task".
    threading.Thread(target=slow_worker).start()
    
    print("[Main] Main thread has finished its work and is exiting now.")
    print("[Main] The worker may or may not have finished its task.")
    
    # The main thread exits here. Depending on the OS and timing, the worker
    # thread might be abruptly terminated before it can write to the file.