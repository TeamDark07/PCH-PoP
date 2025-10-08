# /examples/6_implementation_pitfalls/6_5_busy_waiting_spinlocks/good_example.py

import threading
import time

shared_data = []
# --- The Solution: A threading.Event ---
# An Event is a synchronization primitive that allows one thread to signal
# one or more other threads. It is an efficient way to wait for a condition.
data_ready_event = threading.Event()

def producer():
    """A thread that prepares data and then signals an event."""
    print("[Producer] Preparing data...")
    time.sleep(3) # Simulate preparation time
    
    shared_data.append("Important Data")
    
    print("[Producer] Data is ready. Setting the event to wake up the consumer.")
    # .set() changes the internal flag of the event to True and wakes up
    # any threads that are waiting on it.
    data_ready_event.set()

def consumer():
    """A thread that waits efficiently for an event."""
    print("[Consumer] Waiting for data (efficiently)...")
    
    # .wait() blocks the thread until the internal flag of the event is
    # set to True. This is a highly efficient wait; the thread is put to
    # sleep by the OS and consumes no CPU cycles.
    data_ready_event.wait()
        
    print(f"[Consumer] Data has arrived: {shared_data[0]}")

if __name__ == "__main__":
    print("--- Efficient Waiting with `threading.Event` ---")
    
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    start_cpu_time = time.process_time()
    
    consumer_thread.start()
    producer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    end_cpu_time = time.process_time()
    
    print("\n--- Results ---")
    print(f"Total CPU time consumed: {end_cpu_time - start_cpu_time:.4f} seconds.")
    print("The CPU time is now negligible because the consumer thread was sleeping, not spinning.")