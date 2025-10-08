### 2.3: Cancellation & Timeouts Not Handled

A robust concurrent application must be able to handle tasks that take too long or need to be stopped. Without proper handling, a single unresponsive task can cause the entire application to hang.

-   **Timeout:** A mechanism to stop waiting for a single blocking operation after a certain amount of time.
-   **Cancellation:** A mechanism to signal a long-running task that it should stop its work, clean up, and exit gracefully.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a worker thread that simulates a network call to an unresponsive API. The main thread then calls `.join()` on the worker without a timeout. Because the worker function will never return, the `.join()` call will block forever, and the application will hang indefinitely.

*(Note: For demonstration purposes, the script's `.join()` has a short timeout so it can exit and show the error. In a real application without it, the script would never terminate.)*

**To Run:**
```bash
python bad_example.py