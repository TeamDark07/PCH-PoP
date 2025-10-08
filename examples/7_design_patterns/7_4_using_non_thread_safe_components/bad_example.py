# /examples/7_design_patterns/7_4_using_non_thread_safe_components/bad_example.py

import threading
import time
import random

class UnsafeDBClient:
    """
    A simulated database client that is NOT thread-safe.
    It has an internal state that can be corrupted by concurrent access.
    """
    def __init__(self):
        # This internal state is the source of the problem.
        self.last_query = None

    def execute_query(self, query):
        print(f"[{threading.current_thread().name}] Executing query: '{query}'")
        
        # --- The Race Condition is Here ---
        # 1. Set the internal state.
        self.last_query = query
        
        # A context switch here is disastrous. Another thread can call this
        # method and overwrite `self.last_query` before we get a chance to use it.
        time.sleep(random.uniform(0.1, 0.3))
        
        # 2. Use the internal state.
        # We expect `self.last_query` to be the same as the `query` we just set,
        # but another thread may have changed it.
        if self.last_query != query:
            print(f"[{threading.current_thread().name}] 🔴 CORRUPTION! Expected '{query}' but found '{self.last_query}'.")
            return "Error: Corrupted State"
        else:
            print(f"[{threading.current_thread().name}] Query successful.")
            return f"Result for {query}"

def worker(db_client, query):
    """A worker thread that uses the shared database client."""
    db_client.execute_query(query)

if __name__ == "__main__":
    print("--- Using a Non-Thread-Safe Component Concurrently ---")

    # A single instance of the unsafe client is created.
    unsafe_client = UnsafeDBClient()

    queries = ["SELECT * FROM users", "SELECT * FROM products", "SELECT * FROM orders"]
    threads = []
    
    # All threads will share and use the SAME client instance.
    for query in queries:
        thread = threading.Thread(target=worker, args=(unsafe_client, query))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nSimulation finished. Note the data corruption errors.")