# /examples/6_implementation_pitfalls/6_6_misuse_of_concurrent_futures/bad_example.py

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- Workload Definitions ---
def cpu_bound_task(n):
    """A task that is limited by CPU speed."""
    total = 0
    for i in range(n):
        total += i
    return total

def io_bound_task(duration):
    """A task that is limited by waiting for I/O (simulated with sleep)."""
    time.sleep(duration)
    return f"Slept for {duration}s"

# --- Main Simulation ---

if __name__ == "__main__":
    print("--- Misusing `concurrent.futures` Executors ---")

    # --- Mistake 1: Using ThreadPoolExecutor for a CPU-bound task ---
    print("\n[Scenario 1] Running a heavy CPU-bound task with threads...")
    start_time = time.perf_counter()
    # Due to the GIL, these threads cannot run Python code in parallel.
    # The total time will be roughly the sum of individual task times.
    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(cpu_bound_task, 25_000_000)
        f2 = executor.submit(cpu_bound_task, 25_000_000)
        results = f1.result(), f2.result()
    end_time = time.perf_counter()
    print(f"ThreadPoolExecutor (CPU-bound) took: {end_time - start_time:.4f} seconds. (Suboptimal)")

    # --- Mistake 2: Using ProcessPoolExecutor for a fast I/O-bound task ---
    print("\n[Scenario 2] Running many fast I/O-bound tasks with processes...")
    start_time = time.perf_counter()
    # The overhead of creating processes, pickling data, and inter-process
    # communication is high. For many quick I/O tasks, this overhead
    # makes it slower than using threads.
    with ProcessPoolExecutor(max_workers=10) as executor:
        tasks = [0.2] * 10
        results = list(executor.map(io_bound_task, tasks))
    end_time = time.perf_counter()
    print(f"ProcessPoolExecutor (I/O-bound) took: {end_time - start_time:.4f} seconds. (Suboptimal)")