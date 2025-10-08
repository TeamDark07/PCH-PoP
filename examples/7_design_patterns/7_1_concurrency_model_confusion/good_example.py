# /examples/7_design_patterns/7_1_concurrency_model_confusion/good_example.py

import multiprocessing
import time

# --- The Solution: Using multiprocessing primitives ---

def process_worker(key, value, shared_cache, shared_lock):
    """
    This worker function correctly uses shared objects provided by a Manager.
    """
    print(f"[Process {multiprocessing.current_process().pid}] Running...")
    
    # This is a multiprocessing.Lock, which correctly synchronizes
    # access across different processes.
    with shared_lock:
        print(f"[Process {multiprocessing.current_process().pid}] Acquired the shared lock.")
        
        # This is a special 'managed' dictionary. Modifications to it are
        # proxied back to the main Manager process, making them visible
        # to all other processes.
        shared_cache[key] = value
        
        print(f"[Process {multiprocessing.current_process().pid}] Modified the shared cache: {dict(shared_cache)}")
        time.sleep(1)

if __name__ == "__main__":
    print("--- Correct Inter-Process State Sharing ---")
    print("Using multiprocessing's Manager and Lock.\n")
    
    # A Manager is a special process that can create Python objects
    # that can be shared between other processes.
    manager = multiprocessing.Manager()
    
    # Create a managed dictionary and a managed lock.
    shared_cache = manager.dict()
    shared_lock = manager.Lock()
    
    tasks = [('key1', 10), ('key2', 20)]
    processes = []
    
    for key, value in tasks:
        # We must explicitly pass the managed objects to the child processes.
        p = multiprocessing.Process(target=process_worker, args=(key, value, shared_cache, shared_lock))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("\n--- Results ---")
    print(f"Main process cache state: {dict(shared_cache)}")
    print("🟢 SUCCESS: The cache contains the data from all child processes.")