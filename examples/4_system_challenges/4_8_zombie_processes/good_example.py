# /examples/4_system_challenges/4_8_zombie_processes/good_example.py

import multiprocessing
import time
import os
import sys

def child_process_task():
    """A child process that does some work and then exits."""
    print(f"[Child PID: {os.getpid()}] Starting.")
    time.sleep(2)
    print(f"[Child PID: {os.getpid()}] Exiting now.")

if __name__ == "__main__":
    if sys.platform == "win32":
        print("This example is for Unix-like systems. Windows does not create zombie processes in the same way.")
        sys.exit(0)

    print("--- Proper Process Management (No Zombies) ---")
    print(f"[Parent PID: {os.getpid()}] Starting a child process.")
    
    child = multiprocessing.Process(target=child_process_task)
    child.start()
    
    print("[Parent] Child process started.")
    
    # --- The Solution is Here ---
    # The parent process calls child.join(). This has two effects:
    # 1. It blocks the parent until the child process has finished.
    # 2. It "reaps" the child, reading its exit status and allowing the OS
    #    to remove it from the process table.
    print("[Parent] Waiting for the child process to finish by calling .join()...")
    child.join()
    
    print("[Parent] Child process has been joined. No zombie was created.")
    
    # We can sleep here to prove no zombie exists.
    print("[Parent] Sleeping for 10 seconds. Check the process list now; no zombie will be found.")
    time.sleep(10)

    print(f"[Parent PID: {os.getpid()}] Parent is now exiting.")