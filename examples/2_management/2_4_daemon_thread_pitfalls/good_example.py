# /examples/2_management/2_4_daemon_thread_pitfalls/good_example.py

import threading
import time
import os

LOG_FILE = "managed_log.txt"
shutdown_event = threading.Event()

def critical_logger(log_path):
    """
    A robust logger that performs graceful shutdown when signaled.
    """
    print("[Logger] Non-daemon thread starting...")
    with open(log_path, 'w') as f:
        f.write("--- APPLICATION START ---\n")
        
        entry_num = 1
        # The logger works until the shutdown event is set.
        while not shutdown_event.is_set():
            f.write(f"Log entry {entry_num}\n")
            f.flush()
            print(f"[Logger] Wrote log entry {entry_num}")
            entry_num += 1
            # Wait for 0.5 seconds, or until the event is set
            shutdown_event.wait(timeout=0.5)
            
        # --- This critical cleanup step is now guaranteed to run ---
        f.write("--- APPLICATION SHUTDOWN CLEANLY ---\n")
        
    print("[Logger] Non-daemon thread finished gracefully.")


if __name__ == "__main__":
    # Clean up file from previous runs
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    print("[Main] Starting a critical logger as a managed, non-daemon thread.")
    
    # --- The Correct Approach ---
    # The thread is a normal (non-daemon) thread.
    logger_thread = threading.Thread(target=critical_logger, args=(LOG_FILE,))
    logger_thread.start()
    
    print("[Main] Main thread is working for 1.2 seconds...")
    time.sleep(1.2)
    
    print("[Main] Main thread signaling logger to shut down.")
    shutdown_event.set() # Signal the worker
    
    print("[Main] Waiting for logger to finish...")
    logger_thread.join() # Wait for it to exit cleanly
    
    print("[Main] Main thread is exiting now.")