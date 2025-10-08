# /examples/2_management/2_1_resource_leaks/bad_example.py

import threading
import time
import os

# A global set to simulate tracking of active system resources.
# In a real application, this leak would be at the OS level.
ACTIVE_RESOURCES = set()

def worker(file_path):
    """
    A worker that opens a file but fails to close it if an error occurs.
    """
    print(f"[{threading.current_thread().name}] Opening file: {file_path}")
    
    # --- The Leak is Here ---
    # The file is opened, but the .close() call is never reached
    # because an exception is raised before it.
    
    file_handle = open(file_path, 'w')
    ACTIVE_RESOURCES.add(file_path) # Track the opened resource
    
    # Simulate some work
    file_handle.write("Hello from the worker thread!")
    time.sleep(1)

    # Simulate a critical failure during processing
    raise ValueError("A simulated error occurred in the worker!")
    
    # This cleanup code is never executed
    # file_handle.close()
    # ACTIVE_RESOURCES.remove(file_path)
    # print(f"[{threading.current_thread().name}] Closed file: {file_path}")


if __name__ == "__main__":
    FILENAME = "temp_resource_file.txt"
    
    worker_thread = threading.Thread(target=worker, args=(FILENAME,), name="Worker")
    worker_thread.start()
    
    # Wait for the thread to finish (it will terminate due to the exception)
    worker_thread.join()

    print("\n--- Resource Leak Example ---")
    print(f"Thread '{worker_thread.name}' has finished.")
    
    if FILENAME in ACTIVE_RESOURCES:
        print(f"🔴 LEAK DETECTED: Resource '{FILENAME}' is still in the active set.")
        print("The file handle was not closed because the exception was not handled correctly.")
        # Clean up the leaked resource manually for this demonstration
        os.remove(FILENAME) 
        ACTIVE_RESOURCES.remove(FILENAME)
    else:
        print("🟢 No resource leak detected.")
    
    print(f"Final active resources: {ACTIVE_RESOURCES}")