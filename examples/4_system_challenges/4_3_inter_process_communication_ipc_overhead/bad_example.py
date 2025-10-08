# /examples/4_system_challenges/4_3_inter_process_communication_ipc_overhead/bad_example.py

import multiprocessing
import time
import numpy as np

# A large data object. Using NumPy for efficient memory usage,
# but the serialization overhead is still significant.
LARGE_DATA = np.arange(10_000_000)

def worker_process_data(data):
    """
    A worker process that receives data, performs a trivial operation,
    and returns the modified data.
    """
    # The real "work" is trivial. The bottleneck is the data transfer.
    data[0] += 1
    return data

if __name__ == "__main__":
    print("--- IPC Overhead Demonstration (Bad Example) ---")
    print(f"Data size: {LARGE_DATA.nbytes / 1e6:.2f} MB")

    # We use a Pool to manage the worker process.
    # The map function will handle sending the data to the worker and
    # receiving the result back. This involves:
    # 1. Main process pickles (serializes) LARGE_DATA.
    # 2. Data is sent through an OS pipe to the worker.
    # 3. Worker process unpickles the data.
    # 4. Worker does its job.
    # 5. Worker pickles the result.
    # 6. Result is sent back.
    # 7. Main process unpickles the result.
    
    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=1) as pool:
        # We pass the data as an argument, which forces serialization.
        result = pool.map(worker_process_data, [LARGE_DATA])
    end_time = time.perf_counter()

    print(f"Time taken to pass data back and forth: {end_time - start_time:.4f} seconds.")
    print("\nThis time is dominated by the IPC overhead of pickling and transferring the large data object.")