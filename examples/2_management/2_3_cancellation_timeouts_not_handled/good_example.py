# /examples/2_management/2_3_cancellation_timeouts_not_handled/good_example.py

import threading
import time

# A cancellation event that the main thread can use to signal the worker.
cancellation_event = threading.Event()

def long_running_task_with_cancellation():
    """
    Simulates a long-running task that is designed to be cancellable.
    """
    print("[Worker] Starting a long-running, cancellable task...")
    
    iterations = 0
    # The worker periodically checks the cancellation event.
    # This is "cooperative" because the worker must be written to cooperate.
    while not cancellation_event.is_set():
        print(f"[Worker] Working... (iteration {iterations})")
        iterations += 1
        # In a real task, this would be a single step of a larger computation.
        time.sleep(0.5)
        
    print("[Worker] Cancellation signal received. Cleaning up and exiting gracefully.")

def call_api_with_timeout():
    """
    This function demonstrates the simple and effective use of a timeout.
    """
    # We use a dummy Event object here to simulate a blocking network call.
    # In a real library, this would be built-in.
    api_response_event = threading.Event()
    
    print("[API Caller] Calling an API with a 2-second timeout...")
    
    # The .wait() method with a timeout will block for at most 2 seconds.
    # It returns True if the event was set, and False if it timed out.
    finished_in_time = api_response_event.wait(timeout=2)
    
    if finished_in_time:
        print("[API Caller] API call succeeded.")
    else:
        print("[API Caller] API call timed out after 2 seconds!")


if __name__ == "__main__":
    # --- Part 1: Demonstrate Timeout ---
    print("--- 1. Handling Timeouts ---")
    call_api_with_timeout()
    
    print("\n" + "="*40 + "\n")

    # --- Part 2: Demonstrate Cancellation ---
    print("--- 2. Handling Cancellation ---")
    worker_thread = threading.Thread(target=long_running_task_with_cancellation)
    worker_thread.start()
    
    print("[Main] Letting the worker run for 2 seconds...")
    time.sleep(2)
    
    print("[Main] Sending cancellation signal to the worker.")
    # The main thread signals the worker to stop.
    cancellation_event.set()
    
    # Wait for the worker to shut down gracefully.
    worker_thread.join()
    
    print("[Main] Worker has been cancelled and has exited cleanly.")