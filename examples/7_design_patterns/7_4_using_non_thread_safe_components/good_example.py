# /examples/7_design_patterns/7_4_using_non_thread_safe_components/good_example.py

import threading
import time
import random

# The same unsafe client class from the bad example.
class UnsafeDBClient:
    def __init__(self):
        self.last_query = None

    def execute_query(self, query):
        print(f"[{threading.current_thread().name}] Executing query: '{query}'")
        self.last_query = query
        time.sleep(random.uniform(0.1, 0.3))
        if self.last_query != query:
            print(f"[{threading.current_thread().name}] 🔴 CORRUPTION!")
            return "Error: Corrupted State"
        else:
            print(f"[{threading.current_thread().name}] Query successful.")
            return f"Result for {query}"


# --- Solution 1: External Locking ---
def worker_with_external_lock(db_client, lock, query):
    """
    This worker protects access to the shared client with an external lock.
    """
    with lock:
        print(f"\n[{threading.current_thread().name}] Acquired external lock.")
        db_client.execute_query(query)
        print(f"[{threading.current_thread().name}] Released external lock.")


# --- Solution 2 (Recommended): Thread-Local Storage ---
# This object acts like a dictionary where each thread gets its own value for a key.
thread_local_storage = threading.local()

def get_db_client():
    """
    Each thread calls this to get its own, private instance of the client.
    """
    if not hasattr(thread_local_storage, 'db_client'):
        print(f"[{threading.current_thread().name}] Creating a new DB client for this thread.")
        thread_local_storage.db_client = UnsafeDBClient()
    return thread_local_storage.db_client

def worker_with_thread_local(query):
    """
    This worker gets a client from thread-local storage, so there is no sharing.
    """
    client = get_db_client()
    client.execute_query(query)


if __name__ == "__main__":
    queries = ["SELECT * FROM users", "SELECT * FROM products", "SELECT * FROM orders"]

    # --- Run Solution 1 ---
    print("--- Solution 1: Protecting with an External Lock ---")
    unsafe_client = UnsafeDBClient()
    external_lock = threading.Lock()
    threads1 = []
    for query in queries:
        thread = threading.Thread(target=worker_with_external_lock, args=(unsafe_client, external_lock, query))
        threads1.append(thread)
        thread.start()
    for thread in threads1:
        thread.join()
    print("External locking prevented corruption but serialized the work.")

    print("\n" + "="*50 + "\n")

    # --- Run Solution 2 ---
    print("--- Solution 2: Using Thread-Local Storage for Isolation ---")
    threads2 = []
    for query in queries:
        thread = threading.Thread(target=worker_with_thread_local, args=(query,))
        threads2.append(thread)
        thread.start()
    for thread in threads2:
        thread.join()
    print("Thread-local storage provided each thread with its own client,")
    print("allowing for true concurrency without corruption.")