# /examples/4_system_challenges/4_7_signal_handling_in_multiprocessing/bad_example.py

import multiprocessing
import time
import os

# --- This example is primarily for Unix-like systems (Linux, macOS) ---
# --- Windows has a different signal handling mechanism, but the principle ---
# --- of needing to manage child process shutdown remains. ---

CLEANUP_FILE = "temp_cleanup_status.txt"

def worker_process():
    """
    A worker that runs for a while and has a critical cleanup step.
    """
    # Create a file to signal that the process started.
    with open(CLEANUP_FILE, "w") as f:
        f.write("RUNNING")
        
    print(f"[Worker PID: {os.getpid()}] Starting work. Press Ctrl+C in the next 10 seconds.")
    
    try:
        # Simulate a long-running task
        for i in range(10):
            print(f"[Worker PID: {os.getpid()}] Working... ({i+1}/10)")
            time.sleep(1)
            
        # This is the normal, successful exit path.
        with open(CLEANUP_FILE, "w") as f:
            f.write("CLEANUP_SUCCESS")
        print(f"[Worker PID: {os.getpid()}] Finished work normally.")

    except KeyboardInterrupt:
        # --- This block is NEVER reached in the child process ---
        # The SIGINT signal is not sent to the child process by default.
        print(f"[Worker PID: {os.getpid()}] Caught KeyboardInterrupt! Should not happen.")

    finally:
        # The goal is for this block to run, but it won't on Ctrl+C.
        if os.path.exists(CLEANUP_FILE):
             with open(CLEANUP_FILE, "r") as f:
                if f.read() != "CLEANUP_SUCCESS":
                     with open(CLEANUP_FILE, "w") as f_write:
                         f_write.write("CLEANUP_FINALLY_RUN")
        print(f"[Worker PID: {os.getpid()}] 'finally' block executed.")


if __name__ == "__main__":
    if os.path.exists(CLEANUP_FILE):
        os.remove(CLEANUP_FILE)

    print(f"[Main PID: {os.getpid()}] Starting worker process.")
    p = multiprocessing.Process(target=worker_process)
    p.start()
    
    try:
        # Wait for the process to finish
        p.join()
    except KeyboardInterrupt:
        print(f"\n[Main PID: {os.getpid()}] Caught KeyboardInterrupt! Main process is exiting.")
        # The main process exits, but the child is left as an orphan.
        # The OS will eventually kill the orphan, preventing its 'finally' block.
        
    time.sleep(1) # Give a moment to check the file status
    
    if os.path.exists(CLEANUP_FILE):
        with open(CLEANUP_FILE, 'r') as f:
            status = f.read()
        print(f"\nFinal status of cleanup file: '{status}'")
        if status == "RUNNING":
            print("🔴 The worker's cleanup code did NOT run.")
        os.remove(CLEANUP_FILE)
    else:
        print("Cleanup file was not created.")