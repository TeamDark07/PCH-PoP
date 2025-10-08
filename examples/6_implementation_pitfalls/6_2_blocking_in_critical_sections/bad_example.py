# /examples/6_implementation_pitfalls/6_2_blocking_in_critical_sections/bad_example.py

import threading
import time
import requests

# A shared cache and a lock to protect it.
shared_cache = {}
cache_lock = threading.Lock()

def fetch_and_cache(url):
    """
    Fetches data from a URL and updates the cache.
    This version holds the lock during the slow network call.
    """

    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Attempting to acquire lock...")

    # --- The Problem is Here ---
    # The lock is acquired BEFORE the slow, blocking I/O operation.
    with cache_lock:
        print(f"[{thread_name}] Acquired lock.")
        
        # Check if data is already in cache
        if url in shared_cache:
            print(f"[{thread_name}] Cache hit for {url}.")
            return shared_cache[url]
            
        print(f"[{thread_name}] Cache miss. Fetching {url} while holding the lock...")
        
        # This is a slow, blocking network call. The entire application's
        # ability to access the cache is stalled while we wait.
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            shared_cache[url] = data
            print(f"[{thread_name}] Cached data for {url}.")
        except requests.RequestException as e:
            print(f"[{thread_name}] Failed to fetch {url}: {e}")
            
        print(f"[{thread_name}] Releasing lock.")
    return

if __name__ == "__main__":
    URL = "https://httpbin.org/delay/2" # An API that takes 2 seconds to respond
    
    print("--- Blocking in a Critical Section Demonstration ---")
    
    # We start two threads that will try to access the same resource.
    thread1 = threading.Thread(target=fetch_and_cache, args=(URL,), name="Thread-A")
    thread2 = threading.Thread(target=fetch_and_cache, args=(URL,), name="Thread-B")
    
    start_time = time.perf_counter()
    
    thread1.start()
    time.sleep(0.1) # Ensure Thread-A gets the lock first
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    end_time = time.perf_counter()
    
    print("\n--- Results ---")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    print("\nThe total time is over 2 seconds because Thread-B had to wait for Thread-A's")
    print("slow network call to finish before it could even check the cache.")