### 2.2: Orphaned Tasks / Processes

An **orphaned task** is a thread or process that is started without a proper management plan for its lifecycle. This is often called a "fire-and-forget" approach.

The primary danger of orphaning is that the main program might exit before the background task has finished its critical work. This can lead to incomplete operations, data corruption, or silent failures that are difficult to debug.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a worker thread that takes two seconds to write a confirmation message to a file. However, the main thread does not wait for the worker. It starts the thread and exits immediately. This creates a race between the worker finishing its job and the main program terminating.

**To Run:**
```bash
python bad_example.py