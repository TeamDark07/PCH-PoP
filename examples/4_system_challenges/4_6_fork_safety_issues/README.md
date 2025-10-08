### 4.6: Fork Safety Issues

Using the low-level `os.fork()` system call is powerful, but it is fraught with danger, especially in complex applications. One of the most common and surprising issues relates to **buffered I/O**.

When you `fork` a process, the child process receives a complete copy of the parent's memory. This includes the in-memory buffers used by standard libraries for I/O (like `stdout`, `stdin`, `stderr`). If data is sitting in the parent's buffer at the time of the fork, that data will be duplicated in the child's buffer. When both processes eventually flush their buffers (typically on exit), the buffered data will appear twice.

**Note:** This is a Unix-specific issue. The `os.fork()` call does not exist on Windows.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates the I/O duplication problem.
1.  It prints a message to `stdout` but uses `end=""` to prevent a newline. On most systems, this means the text is held in a buffer and not immediately written to the console.
2.  It then calls `os.fork()`.
3.  Both the parent and the child now have a copy of the buffered message.
4.  When each process exits, it flushes its buffer, causing the message to be printed twice.

**To Run:**
```bash
python bad_example.py