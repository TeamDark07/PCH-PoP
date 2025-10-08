### 1.8: The ABA Problem

The **ABA problem** is a subtle and advanced concurrency issue that occurs in lock-free algorithms that use a **Compare-And-Swap (CAS)** operation.

It happens when a thread:
1.  Reads a shared value **A**.
2.  Gets paused.
3.  While paused, another thread changes the value from **A** to **B**, and then back to **A**.
4.  The first thread resumes, checks the value, and sees it is still **A**. It incorrectly assumes nothing has changed and proceeds with its operation, which may now be invalid and can corrupt data.

This example uses a lock-free stack to demonstrate the problem and its solution.

---

### 🔴 Bad Example (`bad_example.py`)

This script uses `threading.Event`s to force a specific execution order.
-   Thread 1 reads the `head` of the stack, which is Node **A**.
-   Thread 2 interferes: it pops **A**, pops **C**, and then pushes **A** back on top. The `head` pointer once again points to **A**, but the underlying stack is now different.
-   Thread 1 resumes. Its CAS check (`if head == A`) succeeds, and it incorrectly updates the `head` pointer based on its stale information, corrupting the stack.

**To Run:**
```bash
python bad_example.py