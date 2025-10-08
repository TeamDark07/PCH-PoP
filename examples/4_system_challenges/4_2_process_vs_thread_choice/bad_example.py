# /examples/4_system_challenges/4_2_process_vs_thread_choice/bad_example.py

import time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# --- Workload Definitions ---

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

    print("--- Demonstrating Incorrect Concurrency Model Choices ---")

    # --- Mistake 1: Using Processes for a fast I/O-bound task ---
    print(f"\nRunning {NUM_IO_TASKS} fast I/O tasks...")
    start_time = time.perf_counter()
    # The overhead of creating processes and serializing data (pickling) is high.
    # For many small, fast I/O tasks, this overhead dominates the actual work time.
    with ProcessPoolExecutor(max_workers=NUM_IO_TASKS) as executor:
        results = list(executor.map(io_bound_task, URLS))
    end_time = time.perf_counter()
    print(f"Using ProcessPoolExecutor took: {end_time - start_time:.4f} seconds. (Suboptimal)")

    # --- Mistake 2: Using Threads for a CPU-bound task ---
    print(f"\nRunning {NUM_CPU_TASKS} heavy CPU tasks...")
    start_time = time.perf_counter()
    # The Global Interpreter Lock (GIL) prevents threads from running Python
    # bytecode in parallel on multiple CPU cores. There will be no speedup.
    with ThreadPoolExecutor(max_workers=NUM_CPU_TASKS) as executor:
        tasks = [CPU_TASK_LOAD] * NUM_CPU_TASKS
        results = list(executor.map(cpu_bound_task, tasks))
    end_time = time.perf_counter()
    print(f"Using ThreadPoolExecutor took: {end_time - start_time:.4f} seconds. (Suboptimal)")