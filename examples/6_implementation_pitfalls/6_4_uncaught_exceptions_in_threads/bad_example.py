# /examples/6_implementation_pitfalls/6_4_uncaught_exceptions_in_threads/bad_example.py

import threading
import time

def critical_worker():
    """
    A worker that simulates a critical task but is prone to failure.
    """

    print("[Worker] Starting a critical task...")
    time.sleep(1)
    
    # --- The Uncaught Exception is Here ---
    # An unexpected error occurs. Because this is running in a separate thread
    # created with threading.Thread, this exception will NOT be propagated
    # to the main thread. It will simply terminate this thread.
    print("[Worker] An unexpected error is about to happen!")
    raise ValueError("Something went wrong in the worker!")
    
    # This line is never reached.
    # print("[Worker] Task finished successfully.")


if __name__ == "__main__":
    print("--- Uncaught Exception in Thread Demonstration ---")
    
    worker_thread = threading.Thread(target=critical_worker, name="CriticalWorker")
    worker_thread.start()
    
    print("[Main] Worker thread has been started.")
    
    # The main thread continues its work, completely unaware that the
    # worker thread has crashed.
    time.sleep(3)
    
    if worker_thread.is_alive():
        print("[Main] Worker thread is still alive.")
    else:
        print("[Main] Worker thread has terminated.")
        
    print("\n--- Analysis ---")
    print("The main program continued as if nothing was wrong.")
    print("The error in the worker was completely silent, which could lead to")
    print("data corruption or an incomplete application state.")
    
    # The program exits with a success code (0), masking the failure.