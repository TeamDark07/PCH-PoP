# /examples/2_management/2_3_cancellation_timeouts_not_handled/bad_example.py

import threading
import time

def call_slow_api():
    """
    Simulates a network call to an API that is unresponsive.
    This function will block forever.
    """
    print("[Worker] Calling a slow API...")
    
    # In a real scenario, this could be a requests.get() call to a server
    # that is down or a database query that is deadlocked.
    # We simulate it with a very long sleep.
    time.sleep(9999) # Blocks indefinitely
    
    print("[Worker] API call finished.") # This line is never reached


if __name__ == "__main__":
    print("[Main] Starting a worker to call an API.")
    
    worker_thread = threading.Thread(target=call_slow_api)
    
    # We make the worker a daemon thread so that we can exit this script.
    # Otherwise, this script itself would hang forever waiting for the worker.
    # In a real application, a non-daemon thread here would cause a complete freeze.
    worker_thread.daemon = True
    worker_thread.start()
    
    print("[Main] Attempting to join the worker thread...")
    
    # --- The Hang is Here ---
    # The .join() call has no timeout. Because the worker will never finish,
    # the main thread will wait here forever.
    worker_thread.join(timeout=3) # Using a timeout here to make the script runnable

    if worker_thread.is_alive():
        print("\n--- Problem: Application is Hanging ---")
        print("The main thread waited for 3 seconds, but the worker is still running.")
        print("Without a timeout or cancellation, this would be an infinite hang.")
    else:
        print("\nWorker finished (this should not happen in this example).")