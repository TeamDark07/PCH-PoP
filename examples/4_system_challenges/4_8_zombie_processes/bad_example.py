# /examples/4_system_challenges/4_8_zombie_processes/bad_example.py

import multiprocessing
import time
import os
import sys

# --- This example is specific to Unix-like operating systems (Linux, macOS) ---
# --- Windows manages processes differently and does not create zombies in this way ---

def child_process_task():
    """A child process that does some work and then exits."""
    print(f"[Child PID: {os.getpid()}] Starting.")
    time.sleep(2)
    print(f"[Child PID: {os.getpid()}] Exiting now.")
    # The process will exit here.

if __name__ == "__main__":
    if sys.platform == "win32":
        print("This example is for Unix-like systems. Windows does not create zombie processes in the same way.")
        sys.exit(0)

    print("--- Zombie Process Demonstration ---")
    print(f"[Parent PID: {os.getpid()}] Starting a child process.")
    
    child = multiprocessing.Process(target=child_process_task)
    child.start()
    
    print("[Parent] Child process started.")
    
    # --- The Mistake is Here ---
    # The parent process does NOT call child.join().
    # It does not wait for the child to finish or read its exit status.
    
    # The parent will continue its own work (simulated by sleep).
    # During this time, the child will finish and become a zombie.
    print("[Parent] The child process will exit in 2 seconds and become a zombie.")
    print("[Parent] The parent will sleep for 10 seconds, keeping the zombie alive.")
    print("[Parent] Check the process list now using 'ps aux | grep Z' in another terminal.")
    
    time.sleep(10)
    
    # When the parent finally exits, the zombie process will be cleaned up
    # by the operating system's `init` process.
    print(f"[Parent PID: {os.getpid()}] Parent is now exiting, which will clean up the zombie.")