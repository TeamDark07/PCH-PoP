# /examples/3_resource_contention/3_3_starvation/bad_example.py

import threading
import time
import random

# A shared lock that all threads will compete for.
shared_lock = threading.Lock()
stop_event = threading.Event()

def greedy_worker(worker_id):
    """
    A worker that frequently tries to acquire the lock.
    """
    counter = 0
    while not stop_event.is_set():
        with shared_lock:
            counter += 1
            # Hold the lock for a very short time
            time.sleep(0.001)
        # Briefly yield to other threads
        time.sleep(random.uniform(0.001, 0.005))
    print(f"[Greedy Worker {worker_id}] Acquired lock {counter} times.")

def patient_worker():
    """
    A worker that is less aggressive and may be starved.
    """
    print("[Patient Worker] Waiting for a chance to acquire the lock...")
    
    # Try to acquire the lock. With high contention, this might take a very long time.
    acquired = shared_lock.acquire(timeout=4.5) # Use a timeout to avoid infinite block
    
    if acquired:
        print("[Patient Worker] Hooray! I finally acquired the lock!")
        # Simulate doing some important, one-off work
        time.sleep(0.1)
        shared_lock.release()
    else:
        print("[Patient Worker] I was starved and never got the lock. :(")

if __name__ == "__main__":
    NUM_GREEDY_WORKERS = 5
    
    print("--- Starvation Example ---")
    print(f"{NUM_GREEDY_WORKERS} greedy workers will constantly compete for a lock.")
    print("A single patient worker will try to acquire it once.")

    greedy_threads = []
    for i in range(NUM_GREEDY_WORKERS):
        thread = threading.Thread(target=greedy_worker, args=(i,))
        greedy_threads.append(thread)
        thread.start()

    patient_thread = threading.Thread(target=patient_worker)
    patient_thread.start()

    # Let the simulation run for 5 seconds
    time.sleep(5)
    stop_event.set() # Signal greedy workers to stop

    for thread in greedy_threads:
        thread.join()
    patient_thread.join()
    
    print("\nSimulation finished.")