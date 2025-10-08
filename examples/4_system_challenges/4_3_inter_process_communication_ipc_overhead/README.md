### 4.3: Inter-Process Communication (IPC) Overhead

Unlike threads, which share the same memory space, processes have separate memory. To communicate, they must use **Inter-Process Communication (IPC)**, which typically involves:
1.  **Serialization:** The sending process converts the Python object into a stream of bytes (a process called "pickling").
2.  **Transmission:** The operating system sends these bytes from one process to another, often through a pipe.
3.  **Deserialization:** The receiving process converts the bytes back into a Python object ("unpickling").

This entire process has a significant performance cost, especially when sending large objects. The IPC overhead can easily become the main bottleneck in a multiprocessing application.

---

### 🔴 Bad Example (`bad_example.py`)

This script creates a large NumPy array (around 80 MB) and passes it to a worker process. The worker performs a trivial modification and returns the entire array. The vast majority of the execution time is spent on the IPC,pickling, transferring, and unpickling the data,not on the actual work.

**To Run:**
```bash
python bad_example.py