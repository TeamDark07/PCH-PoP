# /examples/1_fundamental_state/1_9_false_sharing/good_example.py

import threading
import time

NUM_THREADS = 4
INCREMENTS = 10_000_000

# A typical CPU cache line is 64 bytes. A Python integer is larger than a C
# integer, but to be safe, we'll space our counters far apart. We'll use a
# padding of 16 integers, which is more than enough to ensure each counter
# gets its own cache line.
PADDING_SIZE = 16

# Create a padded list. Only indices 0, 16, 32, etc., will be used.
padded_counters = [0] * (NUM_THREADS * PADDING_SIZE)

def worker(thread_index):
    """
    Each thread increments its own counter, but the counters are now spaced
    far apart in memory. When Thread 0 writes to its counter at index 0,
    it does not affect the cache line used by Thread 1 for its counter at
    index 16. This eliminates false sharing.
    """
    padded_index = thread_index * PADDING_SIZE
    for _ in range(INCREMENTS):
        padded_counters[padded_index] += 1

if __name__ == "__main__":
    threads = []
    
    print("--- False Sharing Demo (Good Performance with Padding) ---")
    print(f"Running {NUM_THREADS} threads, each incrementing {INCREMENTS:,} times...")
    
    start_time = time.perf_counter()

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    # Extract the final counter values for display
    final_counters = [padded_counters[i * PADDING_SIZE] for i in range(NUM_THREADS)]
    
    print(f"Final counters: {final_counters}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print("\nNote the time. It should be significantly faster than the non-padded version.")