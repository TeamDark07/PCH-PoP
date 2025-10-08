# /examples/4_system_challenges/4_1_the_global_interpreter_lock_gil/bad_example.py

import threading
import time

# A simple, CPU-bound function that counts down from a large number.
# This function does pure computation and no I/O.
def cpu_bound_task(count):
    while count > 0:
        count -= 1

def run_sequentially(count_per_task):
    """Run the task sequentially in the main thread."""
    start_time = time.perf_counter()
    cpu_bound_task(count_per_task)
    cpu_bound_task(count_per_task)
    end_time = time.perf_counter()
    print(f"Sequential run took: {end_time - start_time:.4f} seconds.")
    return end_time - start_time

def run_with_threads(count_per_task, num_threads):
    """Run the task using multiple threads."""
    threads = []
    
    start_time = time.perf_counter()
    for _ in range(num_threads):
        thread = threading.Thread(target=cpu_bound_task, args=(count_per_task,))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    end_time = time.perf_counter()
    print(f"Run with {num_threads} threads took: {end_time - start_time:.4f} seconds.")
    return end_time - start_time

if __name__ == "__main__":
    # A large number to ensure the task takes a noticeable amount of time.
    COUNT = 50_000_000
    
    print("--- GIL Demonstration with Threading (CPU-Bound Task) ---")
    print(f"Performing a countdown from {COUNT:,} twice...")

    # Run the task sequentially to establish a baseline.
    sequential_time = run_sequentially(COUNT)
    
    # Run the task with two threads.
    threaded_time = run_with_threads(COUNT, 2)
    
    print("\n--- Analysis ---")
    print("Expected result without GIL: Threaded version should be ~2x faster.")
    print("Actual result with GIL:    Threaded version is roughly the same speed, or even slower.")
    if threaded_time >= sequential_time:
        print("This is because the GIL prevents multiple threads from executing Python bytecode at the same time on different CPU cores.")