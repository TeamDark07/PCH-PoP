# /examples/2_management/2_4_daemon_thread_pitfalls/bad_example.py

import threading
import time
import os

LOG_FILE = "daemon_log.txt"

def critical_logger(log_path):
    """
    A worker that simulates logging important data to a file.
    This task involves opening a resource, writing to it, and closing it.
    """
    print("[Logger] Daemon thread starting...")
    with open(log_path, 'w') as f:
        f.write("--- APPLICATION START ---\n")
        
        # Simulate continuous logging
        for i in range(1, 6):
            f.write(f"Log entry {i}\n")
            f.flush() # Ensure data is written to the OS buffer
            print(f"[Logger] Wrote log entry {i}")
            time.sleep(0.5)
            
        # --- This critical cleanup step is never reached ---
        f.write("--- APPLICATION SHUTDOWN CLEANLY ---\n")
        
    print("[Logger] Daemon thread finished.") # This message is never printed


if __name__ == "__main__":
    # Clean up file from previous runs
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    print("[Main] Starting a critical logger as a daemon thread.")
    
    # Create and start the thread
    logger_thread = threading.Thread(target=critical_logger, args=(LOG_FILE,))
    
    # --- The Pitfall is Here ---
    # By setting daemon=True, we are telling the Python interpreter:
    # "This thread is not important. You can exit the program even if it's
    # still running." The thread will be terminated abruptly.
    logger_thread.daemon = True
    logger_thread.start()
    
    # The main thread does some work and then exits without waiting
    print("[Main] Main thread is working for 1.2 seconds...")
    time.sleep(1.2)
    
    print("[Main] Main thread is exiting now.")
    # The program terminates here.