# /examples/6_implementation_pitfalls/6_4_uncaught_exceptions_in_threads/good_example.py

import threading
import time
from concurrent.futures import ThreadPoolExecutor

def failing_worker(name):
    """A worker designed to fail, now accepting a name for clarity."""
    print(f"[{name}] Starting...")
    time.sleep(1)
    raise ValueError(f"Error in worker {name}!")

# --- Solution 2: Manual Exception Handling ---
def manual_handler_worker(error_queue):
    """
    A worker that manually catches exceptions and reports them
    back to the main thread via a shared queue.
    """
    try:
        print("[Manual Worker] Starting...")
        time.sleep(1)
        raise ValueError("Manual worker failed!")
    except Exception as e:
        print("[Manual Worker] Caught exception, putting it in the queue.")
        error_queue.put(e)


if __name__ == "__main__":
    
    # --- Solution 1 (Recommended): Using ThreadPoolExecutor ---
    print("--- 1. Solution with `concurrent.futures.ThreadPoolExecutor` ---")
    
    # The ThreadPoolExecutor manages threads and their results/exceptions.
    with ThreadPoolExecutor(max_workers=1) as executor:
        print("[Main] Submitting failing_worker to the executor...")
        
        # .submit() returns a Future object, which encapsulates the execution.
        future = executor.submit(failing_worker, "ExecutorWorker")
        
        try:
            # .result() will block until the task is done.
            # CRUCIALLY, if an exception occurred in the worker, .result()
            # will re-raise it here in the main thread.
            result = future.result()
            print(f"[Main] Worker completed with result: {result}")
        except ValueError as e:
            print(f"[Main] 🟢 SUCCESS: Caught exception from the future: {e}")

    print("\n" + "="*50 + "\n")
    
    # --- Solution 2 (Manual): Using a Queue for Error Reporting ---
    print("--- 2. Manual Solution with a Queue ---")
    
    from queue import Queue
    error_queue = Queue()
    
    worker_thread = threading.Thread(target=manual_handler_worker, args=(error_queue,))
    worker_thread.start()
    worker_thread.join()
    
    # After the thread finishes, check the queue for any reported errors.
    if not error_queue.empty():
        err = error_queue.get()
        print(f"[Main] 🟢 SUCCESS: Pulled an error from the queue: {err}")
    else:
        print("[Main] No errors were reported by the worker.")