# /examples/3_resource_contention/3_4_priority_inversion/good_example.py

import threading
import time

# Again, this is a simulation. A real-time OS would handle this automatically.
shared_lock = threading.Lock()

low_prio_has_lock = threading.Event()
high_prio_is_waiting = threading.Event()

def low_priority_task_inheriting():
    """
    Simulates a low-priority task whose priority is temporarily boosted.
    """
    print("[Low Priority] Starting.")
    with shared_lock:
        print("[Low Priority] Acquired the lock.")
        low_prio_has_lock.set()
        
        # The high-priority task is now waiting. The "scheduler" detects this.
        high_prio_is_waiting.wait(timeout=0.5)
        
        # --- Priority Inheritance Simulation ---
        print("[Low Priority] My priority is now BOOSTED to high!")
        print("[Low Priority] I can now run quickly without being preempted by Medium.")
        
        # The sleep is now very short because we are running at high priority.
        time.sleep(0.1) 
        
        print("[Low Priority] Releasing the lock quickly.")
    print("[Low Priority] Finished.")

def medium_priority_task_waiting():
    """
    Simulates a medium-priority task that now has to wait because the
    low-priority task has inherited a higher priority.
    """
    high_prio_is_waiting.wait()
    print("[Medium Priority] Starting.")
    print("[Medium Priority] Cannot run yet, because Low Prio is boosted.")
    
    # We wait for the lock to be released.
    shared_lock.acquire()
    shared_lock.release()
    
    print("[Medium Priority] Can run now. Finished.")

def high_priority_task():
    """Simulates the high-priority task."""
    print("[High Priority] Starting, needs the lock.")
    low_prio_has_lock.wait()
    
    start_wait_time = time.perf_counter()
    print("[High Priority] Is now waiting for the lock...")
    high_prio_is_waiting.set()
    
    with shared_lock:
        end_wait_time = time.perf_counter()
        print("[High Priority] Acquired the lock.")
        wait_duration = end_wait_time - start_wait_time
        print(f"[High Priority] Waited for only {wait_duration:.2f} seconds.")
        if wait_duration < 1:
            print("[High Priority] My wait time was short because priority inheritance worked!")
            
    print("[High Priority] Finished.")

if __name__ == "__main__":
    print("--- Priority Inheritance Simulation (Solution) ---")
    
    low_prio_thread = threading.Thread(target=low_priority_task_inheriting)
    med_prio_thread = threading.Thread(target=medium_priority_task_waiting)
    high_prio_thread = threading.Thread(target=high_priority_task)
    
    low_prio_thread.start()
    high_prio_thread.start()
    med_prio_thread.start()

    low_prio_thread.join()
    med_prio_thread.join()
    high_prio_thread.join()

    print("\nSimulation finished. Note the short wait time for the high-priority task.")