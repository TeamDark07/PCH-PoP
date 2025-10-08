# /examples/6_implementation_pitfalls/6_1_improper_locking_granularity/bad_example.py

import threading
import time

class UserAnalytics:
    """
    A class tracking two independent metrics: user logins and page views.
    """
    def __init__(self):
        self.login_count = 0
        self.page_view_count = 0
        # --- The Problem: A Single, Coarse-Grained Lock ---
        # This one lock protects both login_count and page_view_count.
        self.lock = threading.Lock()

    def increment_logins(self):
        with self.lock:
            print("[Login Thread] Acquired the single lock to update logins.")
            time.sleep(1) # Simulate work
            self.login_count += 1
            print("[Login Thread] Releasing the single lock.")

    def increment_page_views(self):
        with self.lock:
            print("[PageView Thread] Acquired the single lock to update page views.")
            time.sleep(1) # Simulate work
            self.page_view_count += 1
            print("[PageView Thread] Releasing the single lock.")


def login_task(analytics):
    analytics.increment_logins()

def page_view_task(analytics):
    analytics.increment_page_views()

if __name__ == "__main__":
    analytics = UserAnalytics()
    
    print("--- Coarse-Grained Locking Demonstration ---")
    
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
    print("\nBecause one lock protected both independent operations, they could not run")
    print("concurrently. The total time is the sum of their individual times (~2s).")