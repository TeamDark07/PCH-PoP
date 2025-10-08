# /examples/1_fundamental_state/1_1_race_condition/bad_example.py

import threading
import time

# A shared object with a value that will be modified by multiple threads.
class SharedCounter:
    """
    A simple counter that is not thread-safe.
    The increment operation (self.value += 1) is not atomic.
    """
    def __init__(self, initial_value=0):
        self.value = initial_value

def increment_counter(counter, increments):
    """
    This function is the target for our threads. It will increment
    the shared counter a specified number of times.
    """
    for _ in range(increments):
        # This is the critical section where the race condition occurs.
        # It involves three separate, non-atomic steps:
        # 1. Read the current value of counter.value.
        # 2. Add 1 to that value.
        # 3. Write the new value back to counter.value.
        #
        # A thread can be interrupted between any of these steps,
        # leading to a "lost update".
        current_value = counter.value
        time.sleep(0.00001) # Small sleep to increase the chance of context switching
        counter.value = current_value + 1


if __name__ == "__main__":
    NUM_THREADS = 10
    INCREMENTS_PER_THREAD = 1000
    EXPECTED_VALUE = NUM_THREADS * INCREMENTS_PER_THREAD

    # Create the shared counter instance
    counter = SharedCounter()
    
    # Create and start the threads
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(
            target=increment_counter,
            args=(counter, INCREMENTS_PER_THREAD)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print the results
    print("--- Race Condition Example ---")
    print(f"Expected final counter value: {EXPECTED_VALUE}")
    print(f"Actual final counter value:   {counter.value}")
    print(f"Difference (Lost Updates):    {EXPECTED_VALUE - counter.value}")
    print("\nBecause the increment operation was not atomic, many updates were lost.")