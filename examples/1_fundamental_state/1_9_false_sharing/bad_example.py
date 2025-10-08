# /examples/1_fundamental_state/1_9_false_sharing/bad_example.py

import threading
import time

# --- A Note on This Example ---
# False sharing is a hardware-level performance issue. Its effects can vary
# dramatically based on CPU architecture, the number of cores, and the
# specific Python version and OS. This example is designed to make the
# problem as apparent as possible.

NUM_THREADS = 4  # Best to match the number of physical cores
INCREMENTS = 10_000_000

# Create a list of counters. These will be allocated contiguously in memory,
# making it highly likely that multiple counters will fall on the same
# 64-byte CPU cache line.
counters = [0] * NUM_THREADS

def worker(thread_index):
    """
    Each thread increments its own independent counter.
    However, because counters[0], counters[1], etc., are adjacent in memory,
    when Thread 0 writes to its counter, it invalidates the cache line for
    Thread 1, and vice-versa. This is "false sharing".
    """
    for _ in range(INCREMENTS):
        counters[thread_index] += 1

if __name__ == "__main__":
    threads = []
    
    print("--- False Sharing Demo (Bad Performance) ---")
    print(f"Running {NUM_THREADS} threads, each incrementing {INCREMENTS:,} times...")
    
    start_time = time.perf_counter()

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    print(f"Final counters: {counters}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print("\nNote the time. It is slowed down by cache line contention.")