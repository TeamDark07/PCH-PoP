# /examples/6_implementation_pitfalls/6_1_improper_locking_granularity/good_example.py

import threading
import time

class UserAnalytics:
    """
    A class with correctly grained locks for its independent metrics.
    """
    def __init__(self):
        self.login_count = 0
        self.page_view_count = 0
        # --- The Solution: Fine-Grained Locks ---
        # Each independent piece of data is protected by its own lock.
        self.login_lock = threading.Lock()
        self.page_view_lock = threading.Lock()

    def increment_logins(self):
        # This method only acquires the lock for login data.
        with self.login_lock:
            print("[Login Thread] Acquired the login_lock.")
            time.sleep(1) # Simulate work
            self.login_count += 1
            print("[Login Thread] Releasing the login_lock.")

    def increment_page_views(self):
        # This method only acquires the lock for page view data.
        with self.page_view_lock:
            print("[PageView Thread] Acquired the page_view_lock.")
            time.sleep(1) # Simulate work
            self.page_view_count += 1
            print("[PageView Thread] Releasing the page_view_lock.")


def login_task(analytics):
    analytics.increment_logins()

def page_view_task(analytics):
    analytics.increment_page_views()

if __name__ == "__main__":
    analytics = UserAnalytics()
    
    print("--- Fine-Grained Locking Demonstration ---")
    
    login_thread = threading.Thread(target=login_task, args=(analytics,))
    page_view_thread = threading.Thread(target=page_view_task, args=(analytics,))
    
    start_time = time.perf_counter()
    
    login_thread.start()
    page_view_thread.start()
    
    login_thread.join()
    page_view_thread.join()
    
    end_time = time.perf_counter()
    
    print("\n--- Results ---")
    print(f"Final logins: {analytics.login_count}, Final page views: {analytics.page_view_count}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    print("\nBecause each operation had its own lock, they could run concurrently.")
    print("The total time is now based on the longest single operation (~1s).")