# /examples/4_system_challenges/4_6_fork_safety_issues/good_example.py

import os
import sys
import multiprocessing

# This example also only runs on Unix-like systems for the os.fork() part.

def safe_fork_with_flush():
    """
    Solution 1: Manually flush all I/O buffers before forking.
    """
    print("--- Solution 1: Flushing Buffers Before Fork ---")

    # 1. Write to the buffer.
    print("This message is in the buffer...", end="")
    
    # 2. Explicitly flush the buffer to the terminal BEFORE forking.
    sys.stdout.flush()
    
    # 3. Now, fork the process.
    #    The child's copy of the buffer will be empty, so no duplication occurs.
    pid = os.fork()

    if pid == 0:
        # Child Process
        print(f"\n[Child PID: {os.getpid()}] I am the child. No duplicated output.")
    else:
        # Parent Process
        print(f"\n[Parent PID: {os.getpid()}] I am the parent.")
        os.waitpid(pid, 0)

def recommended_approach_spawn():
    """
    Solution 2: Use the high-level 'multiprocessing' module with a safe start method.
    """
    print("\n--- Solution 2: Using 'multiprocessing' with 'spawn' ---")
    
    # This works on all platforms.
    # The 'spawn' method creates a clean new process without inheriting
    # problematic state like I/O buffers.
    
    # Set the start method if the platform supports it.
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        # Already set, or on a system where it's the only option.
        pass

    print("This message is printed only by the parent.")
    
    p = multiprocessing.Process(target=lambda: print(f"[Child PID: {os.getpid()}] Hello from the spawned process."))
    p.start()
    p.join()
    
    print("The output is clean and predictable.")

if __name__ == "__main__":
    if sys.platform == "win32":
        # On Windows, we can only show the recommended 'spawn' approach.
        recommended_approach_spawn()
    else:
        # On Unix, we can show both solutions.
        safe_fork_with_flush()
        recommended_approach_spawn()