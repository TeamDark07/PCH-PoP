# /examples/2_management/2_1_resource_leaks/good_example.py

import threading
import time
import os

# We still use this for demonstration, to prove the resource was cleaned up.
ACTIVE_RESOURCES = set()

def worker(file_path):
    """
    A robust worker that uses a 'with' statement to guarantee resource cleanup.
    """
    print(f"[{threading.current_thread().name}] Opening file: {file_path}")
    
    try:
        # The 'with' statement is the Pythonic solution for resource management.
        # It automatically calls the __enter__ and __exit__ methods of the
        # file object. The __exit__ method, which closes the file, is
        # guaranteed to be called even if an exception occurs inside the block.
        with open(file_path, 'w') as file_handle:
            ACTIVE_RESOURCES.add(file_path)
            
            file_handle.write("Hello from the worker thread!")
            time.sleep(1)

            raise ValueError("A simulated error occurred, but the resource is safe!")

    except ValueError as e:
        print(f"[{threading.current_thread().name}] Caught an expected error: {e}")
    finally:
        # This 'finally' block demonstrates that cleanup happened.
        # Even though the error occurred, the 'with' statement already closed the file.
        if file_path in ACTIVE_RESOURCES:
             # This part of the code is not strictly necessary for the 'with' statement's
             # functionality but helps in our demonstration.
             ACTIVE_RESOURCES.remove(file_path)
        print(f"[{threading.current_thread().name}] Cleanup complete. File handle guaranteed to be closed.")


if __name__ == "__main__":
    FILENAME = "temp_resource_file.txt"
    
    worker_thread = threading.Thread(target=worker, args=(FILENAME,), name="Worker")
    worker_thread.start()
    worker_thread.join()

    print("\n--- Safe Resource Management Example ---")
    print(f"Thread '{worker_thread.name}' has finished.")

    if FILENAME in ACTIVE_RESOURCES:
        print("🔴 LEAK DETECTED: This should not happen!")
    else:
        print("🟢 No resource leak detected. The 'with' statement worked correctly.")
    
    print(f"Final active resources: {ACTIVE_RESOURCES}")

    # Clean up the created file
    if os.path.exists(FILENAME):
        os.remove(FILENAME)