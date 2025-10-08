### 7.3: Synchronous Fan-Out

**Synchronous Fan-Out** is a common performance anti-pattern where a program needs to perform multiple, independent I/O-bound operations (like network requests or database queries) but executes them sequentially in a loop.

This is highly inefficient because the program spends most of its time waiting for one operation to complete before it can even start the next one. The correct approach is to "fan-out" by starting all the operations concurrently and then "fan-in" by gathering the results as they become available.

---

### 🔴 Bad Example (`bad_example.py`)

This script needs to fetch data from four different API endpoints, each of which takes one second to respond. It uses a standard `for` loop to iterate through the list of URLs and calls `requests.get()` for each one. The program makes the first request, waits a full second for the response, then makes the second request, waits another second, and so on.

**To Run:**
```bash
python bad_example.py