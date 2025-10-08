### 6.1: Improper Locking Granularity

**Locking granularity** refers to the scope of data that a single lock is responsible for protecting. Choosing the right granularity is a critical design decision that balances simplicity, performance, and safety.

-   **Coarse-Grained Locking:** Using a single lock to protect a large amount of data, including unrelated components.
    -   **Pro:** Simple to implement.
    -   **Con:** Severely limits concurrency, as threads are blocked even when they want to access independent parts of the data. This creates a performance bottleneck.

-   **Fine-Grained Locking:** Using many small locks to protect individual pieces of data.
    -   **Pro:** Allows for maximum concurrency and performance.
    -   **Con:** More complex to manage and dramatically increases the risk of deadlocks if multiple locks need to be acquired at once.

The goal is to find a balance: group related data under a single lock, but use separate locks for data that can be modified independently.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates **coarse-grained locking**. A `UserAnalytics` class has two independent counters: `login_count` and `page_view_count`. However, a single, global lock is used to protect both.

When one thread wants to increment the login count, it acquires the lock, which blocks another thread from incrementing the page view count, even though these operations are completely unrelated. This serializes the execution and kills performance.

**To Run:**
```bash
python bad_example.py