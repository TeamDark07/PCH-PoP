### 4.7: Signal Handling in Multiprocessing

On Unix-like systems (Linux, macOS), signals are the primary mechanism for communicating events to processes. The most common one is `SIGINT`, which is sent when you press **Ctrl+C**.

A critical pitfall in multiprocessing is that this signal is **only delivered to the main parent process**. It is not automatically propagated to any child processes you have started. This can lead to "zombie" or "orphan" processes if not handled correctly. The child process continues to run after the parent exits, until it is abruptly killed by the operating system, preventing any graceful cleanup.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a worker process that runs a 10-second loop. The worker has a `finally` block for critical cleanup.
1.  You run the script.
2.  Within 10 seconds, you press Ctrl+C.
3.  The main process catches the `KeyboardInterrupt`, prints a message, and exits.
4.  The child process is orphaned. It continues running for a moment and then is terminated by the OS. Its `finally` block for cleanup is **never executed**.

**To Run:**
```bash
python bad_example.py