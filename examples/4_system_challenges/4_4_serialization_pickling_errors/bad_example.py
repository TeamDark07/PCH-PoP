# /examples/4_system_challenges/4_4_serialization_pickling_errors/good_example.py

import multiprocessing

# --- Solution 1: Define a top-level function instead of using a lambda ---
# Top-level functions defined with 'def' are always picklable.
def add_ten(x):
    return x + 10

# A global variable to hold the lock, which will be created by each worker.
worker_lock = None

def init_worker():
    """
    An initializer function that runs once per worker process.
    This is the correct place to create process-specific resources like locks.
    """
    global worker_lock
    print("Initializing worker...")
    # Each worker process creates its OWN lock.
    worker_lock = multiprocessing.Lock()

def worker(task, value):
    """
    The worker now receives picklable objects (a function and an integer).
    It uses the lock that was created in its own process.
    """
    print("Worker started...")
    with worker_lock:
        result = task(value)
        print(f"Worker finished with result: {result}")
    return result

if __name__ == "__main__":
    print("--- Avoiding Pickling Errors ---")
    
    # The arguments are now a picklable function and a simple integer.
    args_to_send = [
        (add_ten, 5)
    ]
    
    print("Sending picklable objects to the worker process...")
    
    try:
        # We use the 'initializer' argument to set up the lock in each worker.
        with multiprocessing.Pool(processes=1, initializer=init_worker) as pool:
            results = pool.starmap(worker, args_to_send)
        
        print("\n🟢 SUCCESS! The operation completed.")
        print(f"   Final results: {results}")

    except Exception as e:
        print("\n🔴 ERROR CAUGHT! This should not have happened.")
        print(f"   Type: {type(e).__name__}")
        print(f"   Reason: {e}")