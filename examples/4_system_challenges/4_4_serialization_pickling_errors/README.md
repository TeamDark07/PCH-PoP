### 4.4: Serialization (Pickling) Errors

When you use `multiprocessing`, any data or functions sent from the main process to a worker process must be **serialized**. The default serialization protocol in Python is called **pickle**.

However, not all Python objects can be pickled. Objects that are tightly bound to the runtime state of a specific process, such as **locks, file handles, database connections, and some `lambda` functions**, are unpicklable. Attempting to send them to another process will result in a `PicklingError`.

---

### 🔴 Bad Example (`bad_example.py`)

This script defines a `worker` function that expects a `lambda` function and a `threading.Lock` object as arguments. The main process attempts to create these objects and send them to a worker in a `multiprocessing.Pool`.

The `pool.starmap` call will fail immediately when it tries to pickle these objects for transmission, raising an exception in the main process.

**To Run:**
```bash
python bad_example.py