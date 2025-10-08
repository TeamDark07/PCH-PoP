# /examples/7_design_patterns/7_3_synchronous_fan_out/bad_example.py

import time
import requests

# A list of API endpoints that each take about 1 second to respond.
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
    print("--- Synchronous Fan-Out Demonstration (Slow) ---")
    print("Fetching 4 URLs one by one in a simple for loop.")
    
    start_time = time.perf_counter()
    
    # --- The Anti-Pattern: Sequential Execution ---
    # The program makes one request and waits for it to complete before
    # starting the next one. This is highly inefficient.
    results = []
    for url in URLS:
        results.append(fetch_url(url))
        
    end_time = time.perf_counter()
    
    print("\n--- Results ---")
    print(f"Final results: {results}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    print("\nThe total time is the sum of all individual request times (~4s).")