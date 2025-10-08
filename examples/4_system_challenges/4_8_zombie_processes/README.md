### 4.8: Zombie Processes

On Unix-like operating systems (Linux, macOS), a **zombie process** (or "defunct" process) is a process that has completed its execution but still has an entry in the process table.

This occurs when a child process terminates, but its parent process has not yet "reaped" it by reading its exit status. The zombie process itself uses no memory or CPU, but its entry in the process table consumes a slot. A large number of zombies can exhaust the process table, preventing new processes from being created.

The parent process is **always** responsible for cleaning up its children.

**Note:** This is a Unix-specific concept. Windows handles process termination differently and does not leave zombie processes in the same way.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a child process that runs for two seconds and then exits. The parent process, however, never calls the `.join()` method. It continues to run for another 10 seconds. During this window, the terminated child process exists as a zombie.

**To Run:**
1.  Open a terminal and run the script:
    ```bash
    python bad_example.py
    ```
2.  **Quickly**, within the next 10 seconds, open a **second terminal** and run this command to find zombie processes:
    ```bash
    ps aux | grep Z
    ```
    (The `Z` in the state column indicates a zombie process).

**Expected Output:**
In the script's terminal, you will see it prompt you to check the process list. In the second terminal, the `ps` command will show an entry for the `bad_example.py` child process with a `Z` or `defunct` status, confirming it's a zombie.