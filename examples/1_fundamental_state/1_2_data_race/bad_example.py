# /examples/1_fundamental_state/1_2_data_race/bad_example.py

import threading
import random
import time

# A shared list that will be modified by multiple threads.
# This is our shared memory location.
shared_data = [0] * 10

def worker(thread_id, data):
    """
    This function simulates work that modifies the shared data structure.
    Each thread will iterate through the list and add its ID to each element.
    """
    print(f"Thread {thread_id} starting...")
    for i in range(len(data)):
        # --- This is the location of the data race ---
        # The operation `data[i] += thread_id` is not atomic.
        # It breaks down into:
        # 1. Read the value of data[i].
        # 2. Add thread_id to it.
        # 3. Write the new value back to data[i].
        #
        # If Thread 1 reads data[i] (value 0) and is then paused,
        # Thread 2 can read the same data[i] (still 0), calculate its new
        # value, and write it back. When Thread 1 resumes, it will overwrite
        # the work done by Thread 2, leading to data corruption.
        value = data[i]
        # A small random sleep increases the probability of a context switch
        # happening in the middle of the operation, making the data race obvious.
        time.sleep(random.uniform(0.0, 0.001))
        data[i] = value + thread_id
    print(f"Thread {thread_id} finished.")

if __name__ == "__main__":
    NUM_THREADS = 5
    threads = []
    
    # The expected value for each element in the list is the sum of all thread IDs.
    # For 5 threads with IDs 1 through 5, the sum is 1+2+3+4+5 = 15.
    expected_sum = sum(range(1, NUM_THREADS + 1))
    expected_data = [expected_sum] * len(shared_data)

    # Create and start threads
    for i in range(NUM_THREADS):
        # We pass a unique ID (starting from 1) to each thread.
        thread = threading.Thread(target=worker, args=(i + 1, shared_data))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete their work
    for thread in threads:
        thread.join()

    # Print the results
    print("\n--- Data Race Example ---")
    print(f"Expected final list: {expected_data}")
    print(f"Actual final list:   {shared_data}")
    print("\nDue to the data race, the actual list is corrupted and does not match the expected result.")