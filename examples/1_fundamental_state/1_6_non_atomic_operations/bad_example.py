# /examples/1_fundamental_state/1_6_non_atomic_operations/bad_example.py

import threading
import dis

class SharedCounter:
    """A simple shared counter, vulnerable to non-atomic operations."""
    def __init__(self, initial_value=0):
        self.value = initial_value

def increment(counter, increments):
    """Increments the counter's value. The '+=' operation is not atomic."""
    for _ in range(increments):
        # This single line of Python is the source of the problem.
        # It looks atomic, but it is not.
        counter.value += 1

def show_disassembly():
    """Use the 'dis' module to show the bytecode for the increment operation."""
    def sample_increment(x):
        x += 1
    
    print("--- Disassembly of 'x += 1' ---")
    dis.dis(sample_increment)
    print("---------------------------------")
    print("Note the multiple steps: LOAD, INPLACE_ADD, and STORE.")
    print("A thread can be interrupted between any of these steps.\n")

if __name__ == "__main__":
    # First, let's prove that the operation is not atomic.
    show_disassembly()

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

    print("--- Non-Atomic Operation Example ---")
    print(f"Expected final value: {EXPECTED_VALUE}")
    print(f"Actual final value:   {counter.value}")
    print(f"Difference:           {EXPECTED_VALUE - counter.value}")
    print("\nThe final value is incorrect because the 'value += 1' operation is not atomic.")