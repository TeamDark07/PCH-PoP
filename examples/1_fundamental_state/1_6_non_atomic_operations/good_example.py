# /examples/1_fundamental_state/1_6_non_atomic_operations/good_example.py

import threading

class SharedCounter:
    """A thread-safe shared counter using a lock."""
    def __init__(self, initial_value=0):
        self.value = initial_value
        self.lock = threading.Lock()

def increment(counter, increments):
    """
    Safely increments the counter's value by protecting the non-atomic
    operation with a lock.
    """
    for _ in range(increments):
        # The 'with' statement ensures the lock is acquired before the
        # operation and released after.
        with counter.lock:
            # Although 'counter.value += 1' is still multiple bytecode
            # instructions, the lock guarantees that no other thread can
            # execute this block until the current thread is finished.
            # This makes the entire operation effectively atomic.
            counter.value += 1

if __name__ == "__main__":
    NUM_THREADS = 10
    INCREMENTS_PER_THREAD = 100000
    EXPECTED_VALUE = NUM_THREADS * INCREMENTS_PER_THREAD

    counter = SharedCounter()
    
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=increment, args=(counter, INCREMENTS_PER_THREAD))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("--- Atomic Operation Example with Lock ---")
    print(f"Expected final value: {EXPECTED_VALUE}")
    print(f"Actual final value:   {counter.value}")
    print(f"Difference:           {EXPECTED_VALUE - counter.value}")
    print("\nBy wrapping the operation in a lock, we enforce atomicity and get the correct result.")