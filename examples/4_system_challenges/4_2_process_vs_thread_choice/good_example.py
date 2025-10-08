# /examples/4_system_challenges/4_2_process_vs_thread_choice/good_example.py

import time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- Workload Definitions (same as bad_example.py) ---

def io_bound_task(url):
    """A task that is limited by network speed (I/O)."""
    try:
        requests.get(url, timeout=2)
        return "Success"
    except requests.exceptions.RequestException:
        return "Failed"

def cpu_bound_task(n):
    """A task that is limited by CPU speed."""
    count = 0
    for i in range(n):
        count += i
    return count

# --- Main Simulation ---

if __name__ == "__main__":
    NUM_IO_TASKS = 20
    NUM_CPU_TASKS = 4
    CPU_TASK_LOAD = 10_000_000
    URLS = ["https://httpbin.org/delay/0.5"] * NUM_IO_TASKS

    print("--- Demonstrating Correct Concurrency Model Choices ---")

    # --- Correct Choice 1: Using Threads for I/O-bound tasks ---
    print(f"\nRunning {NUM_IO_TASKS} fast I/O tasks...")
    start_time = time.perf_counter()
    # Threads are lightweight. The GIL is released during the network wait,
    # allowing other threads to make their requests. This is highly efficient.
    with ThreadPoolExecutor(max_workers=NUM_IO_TASKS) as executor:
        results = list(executor.map(io_bound_task, URLS))
    end_time = time.perf_counter()
    print(f"Using ThreadPoolExecutor took: {end_time - start_time:.4f} seconds. (Optimal)")

    # --- Correct Choice 2: Using Processes for CPU-bound tasks ---
    print(f"\nRunning {NUM_CPU_TASKS} heavy CPU tasks...")
    start_time = time.perf_counter()
    # Processes bypass the GIL, allowing tasks to run in true parallel
    # on different CPU cores, resulting in a significant speedup.
    with ProcessPoolExecutor(max_workers=NUM_CPU_TASKS) as executor:
        tasks = [CPU_TASK_LOAD] * NUM_CPU_TASKS
        results = list(executor.map(cpu_bound_task, tasks))
    end_time = time.perf_counter()
    print(f"Using ProcessPoolExecutor took: {end_time - start_time:.4f} seconds. (Optimal)")