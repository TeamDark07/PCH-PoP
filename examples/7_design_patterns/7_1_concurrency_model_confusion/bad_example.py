# /examples/7_design_patterns/7_1_concurrency_model_confusion/bad_example.py

import multiprocessing
import threading
import time

# --- The Mistake: Using threading primitives with multiprocessing ---

# A standard Python dictionary, intended to be a shared cache.
shared_cache = {}

# A standard threading.Lock, intended to protect the cache.
# This lock will NOT work across processes.
shared_lock = threading.Lock()

def process_worker(key, value):
    """
    This worker function runs in a separate process.
    It attempts to modify a global dictionary and use a threading.Lock.
    """
    print(f"[Process {multiprocessing.current_process().pid}] Running...")
    
    # Each process gets its OWN copy of the lock, so this provides
    # no actual protection between processes.
    with shared_lock:
        print(f"[Process {multiprocessing.current_process().pid}] Acquired its local lock.")
        
        # Each process also gets its OWN copy of `shared_cache`.
        # Any modification here will be lost when the process exits.
        shared_cache[key] = value
        
        print(f"[Process {multiprocessing.current_process().pid}] Modified its local cache: {shared_cache}")
        time.sleep(1)

if __name__ == "__main__":
    print("--- Concurrency Model Confusion Demonstration ---")
    print("Using threading's shared-memory patterns with multiprocessing.\n")
    
    tasks = [('key1', 10), ('key2', 20)]
    processes = []
    
    for key, value in tasks:
        # We create new processes, each with a separate memory space.
        p = multiprocessing.Process(target=process_worker, args=(key, value))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("\n--- Results ---")
    print(f"Main process cache state: {shared_cache}")
    print("🔴 FAILURE: The cache is empty.")
    print("The modifications made by the child processes were in their own memory")
    print("spaces and were lost when they exited.")