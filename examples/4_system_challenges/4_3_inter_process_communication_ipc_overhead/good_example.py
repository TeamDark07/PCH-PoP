# /examples/4_system_challenges/4_3_inter_process_communication_ipc_overhead/good_example.py

import multiprocessing
import time
import numpy as np
from multiprocessing import shared_memory

# A global variable to hold the name of the shared memory block.
shared_mem_name = None

def init_worker(shm_name, shape, dtype):
    """
    Initializer for the worker process. It connects to the existing
    shared memory block.
    """
    global shared_array
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    shared_array = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

def worker_process_shared_data(index):
    """
    The worker now operates directly on the shared memory array.
    No data is passed as an argument.
    """
    shared_array[index] += 1
    # No need to return anything, the change is visible in the main process.
    return

if __name__ == "__main__":
    print("--- IPC Overhead Avoidance with Shared Memory (Good Example) ---")
    
    # Create the data
    data = np.arange(10_000_000)
    print(f"Data size: {data.nbytes / 1e6:.2f} MB")
    
    try:
        # 1. Create a shared memory block large enough to hold our data.
        shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
        shared_mem_name = shm.name
        
        # 2. Create a NumPy array that uses the shared memory buffer.
        shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
        
        # 3. Copy our data into the shared memory.
        shared_array[:] = data[:]
        
        start_time = time.perf_counter()
        # The Pool's initializer function connects each worker to the shared memory.
        with multiprocessing.Pool(processes=1, initializer=init_worker, initargs=(shm.name, data.shape, data.dtype)) as pool:
            # We only pass a small index, not the large data array.
            pool.map(worker_process_shared_data, [0])
        end_time = time.perf_counter()
        
        print(f"Time taken using shared memory: {end_time - start_time:.4f} seconds.")
        print("\nThis is significantly faster because only a tiny message (the index) was sent.")
        print(f"Is the change visible? shared_array[0] = {shared_array[0]}")

    finally:
        # 4. Clean up the shared memory block in all cases.
        if shared_mem_name:
            # In the main process, we need to close and unlink the shared memory.
            shm.close()
            shm.unlink()