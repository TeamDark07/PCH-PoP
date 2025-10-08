# /examples/3_resource_contention/3_4_priority_inversion/bad_example.py

import threading
import time

# --- A Note on This Example ---
# Python's threading module does not provide a reliable way to set thread
# priorities that maps directly to OS-level priorities.
# This script SIMULATES the behavior of priority inversion to make the
# concept clear. We use events and sleeps to control the execution order
# to mimic a priority-based scheduler's actions.

# A shared resource that requires a lock
shared_lock = threading.Lock()

# Events to control the execution flow for the simulation
low_prio_has_lock = threading.Event()
high_prio_is_waiting = threading.Event()

def low_priority_task():
    """Simulates a low-priority task that acquires a lock."""
    print("[Low Priority] Starting.")
    with shared_lock:
        print("[Low Priority] Acquired the lock.")
        low_prio_has_lock.set() # Signal that the lock is held
        
        # Now, the high-priority task will start and try to get the lock.
        # While the high-priority task is blocked, the medium-priority
        # task will "preempt" us.
        print("[Low Priority] Paused by 'scheduler' (simulating preemption)...")
        time.sleep(3) # This represents the medium-priority task running
        
        print("[Low Priority] Resuming and releasing the lock.")
    print("[Low Priority] Finished.")

def medium_priority_task():
    """
    Simulates a medium-priority task that runs and prevents the
    low-priority task from releasing its lock.
    """
    # This task starts after the high-priority task is already blocked.
    high_prio_is_waiting.wait()
    print("[Medium Priority] Starting and running, preventing Low Prio from running.")
    # The work of this task is represented by the sleep in the low_priority_task
    print("[Medium Priority] Finished.")
    
def high_priority_task():
    """

    Simulates a high-priority task that gets blocked by a lower-priority task.
    """
    print("[High Priority] Starting, needs the lock.")
    # Wait until the low-priority task has the lock
    low_prio_has_lock.wait()
    
    start_wait_time = time.perf_counter()
    print("[High Priority] Is now waiting for the lock...")
    high_prio_is_waiting.set() # Signal that we are now waiting
    
    with shared_lock:
        end_wait_time = time.perf_counter()
        print("[High Priority] FINALLY acquired the lock.")
        wait_duration = end_wait_time - start_wait_time
        print(f"[High Priority] Waited for {wait_duration:.2f} seconds.")
        if wait_duration > 2:
            print("[High Priority] My wait time was long because the Medium Prio task ran!")
            
    print("[High Priority] Finished.")


if __name__ == "__main__":
    print("--- Priority Inversion Simulation ---")
    
    low_prio_thread = threading.Thread(target=low_priority_task)
    med_prio_thread = threading.Thread(target=medium_priority_task)
    high_prio_thread = threading.Thread(target=high_priority_task)
    
    # Start threads in a specific order to simulate the scenario
    low_prio_thread.start()
    high_prio_thread.start()
    med_prio_thread.start()

    low_prio_thread.join()
    med_prio_thread.join()
    high_prio_thread.join()
    
    print("\nSimulation finished. Note the long wait time for the high-priority task.")