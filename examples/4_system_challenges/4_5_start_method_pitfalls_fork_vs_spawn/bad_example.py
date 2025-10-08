# /examples/4_system_challenges/4_5_start_method_pitfalls_fork_vs_spawn/bad_example.py

import multiprocessing
import threading
import time
import sys

# A global lock that a background thread will hold.
background_thread_lock = threading.Lock()

def background_thread_task():
    """A task that acquires a lock and holds it forever."""
    print("[Background Thread] Acquiring lock...")
    background_thread_lock.acquire()
    print("[Background Thread] Lock acquired. Holding it...")
    # This thread will now hold the lock indefinitely.
    time.sleep(9999)

def worker_process_task():
    """A simple task for the worker process."""
    print("[Worker Process] Hello from the worker!")
    return "Success"

if __name__ == "__main__":
    # --- This example will only deadlock on systems that use 'fork' by default (Linux/macOS) ---
    if sys.platform == "win32":
        print("This example is designed for fork-based systems (Linux/macOS).")
        print("On Windows, which uses 'spawn' by default, this code will not deadlock.")
        # We can force 'fork' if we are on a system that supports it.
        # However, for demonstration, we just exit if not on a fork-like system.
        try:
            multiprocessing.get_start_method() == 'fork'
        except Exception as e:
            print(f"Could not determine start method (treating as non-fork): {e}")
            sys.exit(0)

    print("--- 'fork' Start Method Pitfall Demonstration ---")

    # Start a background thread that acquires and holds a lock.
    bg_thread = threading.Thread(target=background_thread_task, daemon=True)
    bg_thread.start()
    time.sleep(1) # Give the thread time to acquire the lock

    print("[Main] Background thread is now holding a lock.")
    print("[Main] Attempting to start a multiprocessing Pool...")

    # --- The Deadlock is Here ---
    # When the Pool creates a new worker process using 'fork', the child
    # process's memory is a copy of the parent's. This includes a copy of
    # `background_thread_lock` in a 'locked' state.
    #
    # However, the child process only has one thread (the main one). The
    # background thread that would release the lock does not exist in the child.
    # When the child's internal machinery tries to use a lock (e.g., for
    # handling tasks), it can deadlock on itself or on this inherited lock.
    try:
        with multiprocessing.Pool(processes=1) as pool:
            # The program will hang here and will likely never print the result.
            result = pool.apply(worker_process_task)
            print(f"[Main] Worker process returned: {result}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

    # The program will likely be stuck and this part won't be reached.
    print("[Main] This line will likely never be printed.")