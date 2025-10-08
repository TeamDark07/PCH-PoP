# /examples/6_implementation_pitfalls/6_5_busy_waiting_spinlocks/bad_example.py

import threading
import time

# A shared list to act as our data queue.
# A boolean flag to signal when data is ready.
shared_data = []
data_ready = False

def producer():
    """A thread that prepares some data after a delay."""
    print("[Producer] Preparing data...")
    time.sleep(3) # Simulate a long preparation time
    
    global shared_data, data_ready
    shared_data.append("Important Data")
    data_ready = True
    
    print("[Producer] Data is ready.")

def consumer():
    """A thread that waits for data using a busy-wait loop."""
    print("[Consumer] Waiting for data...")
    
    # --- The Problem: Busy-Waiting (Spinlock) ---
    # This 'while' loop continuously checks the 'data_ready' flag without
    # pausing or yielding. This will cause this thread to consume 100%
    # of a CPU core, doing no useful work but preventing other processes
    # from using that core.
    while not data_ready:
        pass # Spin wastefully
        
    print(f"[Consumer] Data has arrived: {shared_data[0]}")

if __name__ == "__main__":
    print("--- Busy-Waiting (Spinlock) Demonstration ---")
    
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    # We use os.times() or time.process_time() to measure CPU time,
    # which will be very high for the busy-waiting consumer.
    start_cpu_time = time.process_time()
    
    consumer_thread.start()
    producer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    end_cpu_time = time.process_time()
    
    print("\n--- Results ---")
    print(f"Total CPU time consumed: {end_cpu_time - start_cpu_time:.4f} seconds.")
    print("This high CPU time is due to the consumer thread's wasteful spinning.")