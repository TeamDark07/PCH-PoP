# /examples/1_fundamental_state/1_7_memory_visibility_issues/bad_example.py

import threading
import time

# --- A Note on This Example ---
# Reproducing a memory visibility issue in CPython is very difficult.
# The Global Interpreter Lock (GIL) often implicitly synchronizes memory between
# threads during context switches, hiding the problem.
#
# However, this pattern is NOT safe and can fail in other Python implementations
# (like Jython, IronPython), in C extensions that release the GIL, or on
# certain hardware with weak memory models.
#
# The code below demonstrates the dangerous pattern. It might hang, or it might
# appear to work, but it is fundamentally incorrect.

# A shared flag that the main thread will change.
done = False

def worker():
    """
    A worker thread that spins in a loop, waiting for the 'done' flag.
    This is called a "busy-wait" or "spinlock".
    """
    print("Worker starting, waiting for the flag...")
    
    # In a system with a weak memory model, the worker thread's CPU cache
    # might never be updated with the new value of 'done' written by the
    # main thread. It would see its own cached 'False' value forever.
    while not done:
        # This loop burns 100% of a CPU core and is not guaranteed to see
        # the change to the 'done' flag.
        pass
        
    print("Worker saw the flag and is finishing.")


if __name__ == "__main__":
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    print("Main thread sleeping for 2 seconds...")
    time.sleep(2)

    print("Main thread setting the done flag to True.")
    # This write might only happen in the main thread's CPU cache.
    done = True

    # We use a timeout because the worker_thread may hang indefinitely.
    worker_thread.join(timeout=2)

    if worker_thread.is_alive():
        print("\n--- ERROR: Worker thread is still alive! ---")
        print("This indicates a potential memory visibility issue or that the thread is stuck.")
    else:
        print("\nWorker thread finished correctly (this time).")