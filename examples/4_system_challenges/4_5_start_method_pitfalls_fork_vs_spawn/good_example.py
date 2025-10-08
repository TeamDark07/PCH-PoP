# /examples/4_system_challenges/4_5_start_method_pitfalls_fork_vs_spawn/good_example.py

import multiprocessing
import threading
import time

background_thread_lock = threading.Lock()

def background_thread_task():
    """A task that acquires a lock and holds it."""
    print("[Background Thread] Acquiring lock...")
    background_thread_lock.acquire()
    print("[Background Thread] Lock acquired. Holding it...")
    time.sleep(5) # Hold for a while, then release
    background_thread_lock.release()
    print("[Background Thread] Lock released.")

def worker_process_task():
    """A simple task for the worker process."""
    print("[Worker Process] Hello from the worker!")
    return "Success"

if __name__ == "__main__":
    # --- The Solution: Set the start method to 'spawn' or 'forkserver' ---
    # This must be done at the very beginning of the program's entry point,
    # inside the `if __name__ == "__main__":` block.
    #
    # 'spawn' creates a brand new Python interpreter process. It is slower,
    # but much safer as it does not inherit memory state like locks from the parent.
    try:
        multiprocessing.set_start_method("spawn")
        print("--- 'spawn' Start Method (Safe) Demonstration ---")
    except RuntimeError:
        print("Start method can only be set once. Assuming 'spawn' is default (e.g., on Windows).")


    # Start the background thread just like in the bad example.
    bg_thread = threading.Thread(target=background_thread_task, daemon=True)
    bg_thread.start()
    time.sleep(1) # Give it time to acquire the lock

    print("[Main] Background thread is now holding a lock.")
    print("[Main] Attempting to start a multiprocessing Pool...")

    # --- No Deadlock ---
    # Because the new worker process is 'spawned', it starts fresh.
    # It does not inherit the locked `background_thread_lock` from the
    # parent process's memory space. The pool's internal machinery can
    # operate without any risk of deadlocking on an inherited lock.
    try:
        with multiprocessing.Pool(processes=1) as pool:
            result = pool.apply(worker_process_task)
            print(f"[Main] Worker process returned: {result}")
        
        print("\n🟢 SUCCESS: The program completed without deadlocking.")

    except Exception as e:
        print(f"\n🔴 An error occurred: {e}")