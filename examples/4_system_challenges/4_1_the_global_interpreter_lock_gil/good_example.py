# /examples/4_system_challenges/4_1_the_global_interpreter_lock_gil/good_example.py

import multiprocessing
import time

# The same CPU-bound function as before.
def cpu_bound_task(count):
    while count > 0:
        count -= 1

def run_sequentially(count_per_task):
    """Run the task sequentially in the main process."""
    start_time = time.perf_counter()
    cpu_bound_task(count_per_task)
    cpu_bound_task(count_per_task)
    end_time = time.perf_counter()
    print(f"Sequential run took: {end_time - start_time:.4f} seconds.")
    return end_time - start_time

def run_with_processes(count_per_task, num_processes):
    """
    Run the task using multiple processes to bypass the GIL.
    """
    processes = []
    
    start_time = time.perf_counter()
    for _ in range(num_processes):
        # Create a new Process. Each process has its own Python interpreter
        # and memory, so the GIL of one process does not affect the others.
        process = multiprocessing.Process(target=cpu_bound_task, args=(count_per_task,))
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()
        
    end_time = time.perf_counter()
    print(f"Run with {num_processes} processes took: {end_time - start_time:.4f} seconds.")
    return end_time - start_time

if __name__ == "__main__":
    # A large number to ensure the task takes a noticeable amount of time.
    COUNT = 50_000_000
    
    print("--- Bypassing the GIL with Multiprocessing (CPU-Bound Task) ---")
    print(f"Performing a countdown from {COUNT:,} twice...")
    
    # Establish a baseline.
    sequential_time = run_sequentially(COUNT)
    
    # Run with two processes.
    multiprocessing_time = run_with_processes(COUNT, 2)
    
    print("\n--- Analysis ---")
    print("The multiprocessing version is significantly faster than the sequential version.")
    print("This is because each process runs on a separate CPU core, achieving true parallelism.")
    speedup = sequential_time / multiprocessing_time
    print(f"Speedup factor: {speedup:.2f}x")