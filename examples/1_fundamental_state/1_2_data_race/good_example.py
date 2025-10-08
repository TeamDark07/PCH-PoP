# /examples/1_fundamental_state/1_2_data_race/good_example.py

import threading
import time

# The shared data list.
shared_data = [0] * 10

# A list of locks, one for each corresponding element in shared_data.
# This allows for "fine-grained" locking.
locks = [threading.Lock() for _ in range(len(shared_data))]

def worker(thread_id, data, data_locks):
    """
    This function safely modifies the shared data structure by using a lock
    for each element before accessing it.
    """
    print(f"Thread {thread_id} starting...")
    for i in range(len(data)):
        # By acquiring the specific lock for the index `i`, we ensure that
        # only one thread can modify `data[i]` at any given time.
        #
        # Importantly, another thread (e.g., Thread 2) can simultaneously
        # work on a different element (e.g., data[i+1]) because it will
        # acquire a different lock (locks[i+1]). This allows for maximum
        # parallelism without sacrificing safety.
        with data_locks[i]:
            value = data[i]
            # A small sleep to simulate work inside the critical section.
            time.sleep(0.001)
            data[i] = value + thread_id
    print(f"Thread {thread_id} finished.")


if __name__ == "__main__":
    NUM_THREADS = 5
    threads = []
    
    expected_sum = sum(range(1, NUM_THREADS + 1))
    expected_data = [expected_sum] * len(shared_data)

    # Create and start threads
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(i + 1, shared_data, locks))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print the results
    print("\n--- Thread-Safe Example with Fine-Grained Locks ---")
    print(f"Expected final list: {expected_data}")
    print(f"Actual final list:   {shared_data}")
    print("\nBy using a lock for each element, the data is modified safely and the final result is correct.")