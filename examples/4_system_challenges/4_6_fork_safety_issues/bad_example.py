# /examples/4_system_challenges/4_6_fork_safety_issues/bad_example.py

import os
import sys

# --- This example is specific to Unix-like operating systems (Linux, macOS) ---
# --- It will not run on Windows, which does not have os.fork() ---

def demonstrate_fork_safety_issue():
    """
    Shows how buffered I/O can be duplicated when using os.fork().
    """
    print("--- Fork Safety Issue Demonstration ---")

    # 1. Write to standard output without a newline character.
    #    Python's stdout is typically line-buffered. This means the text
    #    is stored in a memory buffer and is not sent to the terminal yet.
    print("This message is in the buffer...", end="")

    # 2. Fork the process.
    #    The child process gets a complete copy of the parent's memory,
    #    including the I/O buffer containing "This message is in the buffer...".
    pid = os.fork()

    if pid == 0:
        # --- This is the Child Process ---
        print(f"\n[Child PID: {os.getpid()}] I am the child process.")
        # When the child process exits, its copy of the stdout buffer is flushed.
        
    else:
        # --- This is the Parent Process ---
        print(f"\n[Parent PID: {os.getpid()}] I am the parent, created child {pid}.")
        # Wait for the child to finish to keep output clean.
        os.waitpid(pid, 0)
        # When the parent process exits, its copy of the stdout buffer is also flushed.

    # Both processes will now flush their buffers upon exit.


if __name__ == "__main__":
    if sys.platform == "win32":
        print("os.fork() is not available on Windows. This example is for Unix-like systems.")
        sys.exit(0)
    
    demonstrate_fork_safety_issue()
    
    print("\nLook at the output above. The first message was printed twice!")