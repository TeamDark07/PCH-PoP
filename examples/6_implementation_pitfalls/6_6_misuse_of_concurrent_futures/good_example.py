# /examples/6_implementation_pitfalls/6_6_misuse_of_concurrent_futures/good_example.py

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- Workload Definitions (same as bad_example.py) ---

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
    print("--- Correctly Using `concurrent.futures` Executors ---")

    # --- Correct Choice 1: Using ProcessPoolExecutor for a CPU-bound task ---
    print("\n[Scenario 1] Running a heavy CPU-bound task with processes...")
    start_time = time.perf_counter()
    # Processes bypass the GIL, allowing for true parallel execution on
    # multiple CPU cores, resulting in a significant speedup.
    with ProcessPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(cpu_bound_task, 25_000_000)
        f2 = executor.submit(cpu_bound_task, 25_000_000)
        results = f1.result(), f2.result()
    end_time = time.perf_counter()
    print(f"ProcessPoolExecutor (CPU-bound) took: {end_time - start_time:.4f} seconds. (Optimal)")

    # --- Correct Choice 2: Using ThreadPoolExecutor for a fast I/O-bound task ---
    print("\n[Scenario 2] Running many fast I/O-bound tasks with threads...")
    start_time = time.perf_counter()
    # Threads are lightweight and have low overhead. The GIL is released
    # during `time.sleep`, making threads perfect for managing many
    # concurrent I/O operations.
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [0.2] * 10
        results = list(executor.map(io_bound_task, tasks))
    end_time = time.perf_counter()
    print(f"ThreadPoolExecutor (I/O-bound) took: {end_time - start_time:.4f} seconds. (Optimal)")