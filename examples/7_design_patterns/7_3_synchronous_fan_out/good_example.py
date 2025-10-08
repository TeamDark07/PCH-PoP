# /examples/7_design_patterns/7_3_synchronous_fan_out/good_example.py

import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

def fetch_url(url):
    """A simple function to fetch a single URL."""
    print(f"Fetching {url}...")
    try:
        response = requests.get(url)
        print(f"Finished fetching {url}. Status: {response.status_code}")
        return response.status_code
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return "Error"

if __name__ == "__main__":
    print("--- Concurrent Fan-Out Demonstration (Fast) ---")
    print("Fetching 4 URLs concurrently using a ThreadPoolExecutor.")
    
    start_time = time.perf_counter()
    
    results = []
    # --- The Solution: Concurrent Execution ---
    # A ThreadPoolExecutor is perfect for I/O-bound tasks.
    # We submit all the fetch tasks to the pool at once. The threads
    # will run them concurrently.
    with ThreadPoolExecutor(max_workers=len(URLS)) as executor:
        # submit() returns a Future object for each task.
        future_to_url = {executor.submit(fetch_url, url): url for url in URLS}
        
        # as_completed() yields futures as they finish.
        for future in as_completed(future_to_url):
            results.append(future.result())
            
    end_time = time.perf_counter()
    
    print("\n--- Results ---")
    print(f"Final results: {results}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    print("\nThe total time is now close to the time of the single longest request (~1s).")