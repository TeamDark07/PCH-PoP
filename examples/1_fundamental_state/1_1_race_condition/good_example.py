# /examples/1_fundamental_state/1_1_race_condition/good_example.py

import threading

# A shared object that is now thread-safe using a lock.
class SharedCounter:
    """
    A counter that is made thread-safe by using a threading.Lock.
    The lock ensures that the increment operation is atomic.
    """
    def __init__(self, initial_value=0):
        self.value = initial_value
        # Each instance of the counter now has its own lock.
        self.lock = threading.Lock()

def increment_counter(counter, increments):
    """
    This function safely increments the counter by acquiring the lock
    before modifying the shared value.
    """
    for _ in range(increments):
        # The 'with' statement provides a clean way to acquire and release
        # the lock. The block of code inside the 'with' is the
        # critical section. Only one thread can execute this block at a time.
        with counter.lock:
            # These three steps now happen atomically:
            # 1. Read counter.value.
            # 2. Add 1 to it.
            # 3. Write it back.
            # No other thread can interrupt this process.
            current_value = counter.value
            counter.value = current_value + 1


if __name__ == "__main__":
    NUM_THREADS = 10
    INCREMENTS_PER_THREAD = 100000 # Increased to show performance is still good
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
    print("--- Thread-Safe Example with Lock ---")
    print(f"Expected final counter value: {EXPECTED_VALUE}")
    print(f"Actual final counter value:   {counter.value}")
    print(f"Difference (Lost Updates):    {EXPECTED_VALUE - counter.value}")
    print("\nBy using a lock to protect the critical section, the final value is correct.")