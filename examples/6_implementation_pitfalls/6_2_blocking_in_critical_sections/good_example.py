# /examples/6_implementation_pitfalls/6_2_blocking_in_critical_sections/good_example.py

import threading
import time
import requests

shared_cache = {}
cache_lock = threading.Lock()

def fetch_and_cache_optimized(url):
    """
    An optimized version that minimizes the time the lock is held.
    """
    thread_name = threading.current_thread().name

    # --- The Solution is to keep the critical section as small as possible ---

    # First, check the cache. This is a quick read operation.
    print(f"[{thread_name}] Attempting to acquire lock for a quick check...")
    with cache_lock:
        print(f"[{thread_name}] Acquired lock.")
        if url in shared_cache:
            print(f"[{thread_name}] Cache hit. Releasing lock immediately.")
            return shared_cache[url]
    print(f"[{thread_name}] Cache miss. Releasing lock before network call.")

    # The slow, blocking I/O operation is now performed OUTSIDE the lock.
    # While this thread is waiting for the network, other threads can freely
    # acquire the lock to check the cache for other URLs.
    print(f"[{thread_name}] Fetching {url} without holding the lock...")
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except requests.RequestException as e:
        print(f"[{thread_name}] Failed to fetch {url}: {e}")
        return

    # Now, re-acquire the lock for the short, final write operation.
    print(f"[{thread_name}] Attempting to acquire lock for the final write...")
    with cache_lock:
        print(f"[{thread_name}] Acquired lock for final write.")
        shared_cache[url] = data
        print(f"[{thread_name}] Cached data and released lock.")

if __name__ == "__main__":
    URL = "https://httpbin.org/delay/2"
    
    print("--- Optimized Critical Section Demonstration ---")

    thread1 = threading.Thread(target=fetch_and_cache_optimized, args=(URL,), name="Thread-A")
    thread2 = threading.Thread(target=fetch_and_cache_optimized, args=(URL,), name="Thread-B")
    
    start_time = time.perf_counter()
    
    thread1.start()
    time.sleep(0.1)
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    end_time = time.perf_counter()
    
    print("\n--- Results ---")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    print("\nThe total time is ~2 seconds. Thread-B could check the cache while")
    print("Thread-A was busy with its network call (though it found a miss).")
    print("When Thread-B ran again after A finished, its cache check was instant.")