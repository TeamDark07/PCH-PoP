# /examples/6_implementation_pitfalls/6_7_queue_specific_issues/good_example.py

import threading
import queue
import time

def producer(q, num_consumers):
    """Produces items and then sends the correct number of shutdown signals."""
    for i in range(10):
        item = f"Item-{i}"
        print(f"[Producer] Putting '{item}' into the queue.")
        q.put(item)
        time.sleep(0.2)
        
    # --- Solution 1: Correct Shutdown Signaling ---
    # Send one poison pill for each consumer to ensure they all exit.
    print(f"[Producer] All work sent. Putting {num_consumers} poison pills into the queue.")
    for _ in range(num_consumers):
        q.put(None)

def consumer(consumer_id, q):
    """A robust consumer that correctly handles shutdown."""
    # --- Solution 2: Safe use of get_nowait() ---
    # By wrapping the call in a try/except block, we can handle the
    # case where the queue is empty without crashing.
    try:
        initial_item = q.get_nowait()
        print(f"[Consumer-{consumer_id}] (nowait) Got initial item: {initial_item}")
        q.task_done() # Signal that this task is complete
    except queue.Empty:
        print(f"[Consumer-{consumer_id}] (nowait) Found queue empty, proceeding to main loop.")

    while True:
        item = q.get()
        if item is None:
            # We must call task_done() for the poison pill as well,
            # so the main thread's q.join() can complete.
            q.task_done()
            print(f"[Consumer-{consumer_id}] Received poison pill. Exiting.")
            break
        
        print(f"[Consumer-{consumer_id}] Processing '{item}'...")
        time.sleep(0.5)
        # --- Part of Solution 3: The task_done()/join() pattern ---
        # For every item retrieved with .get(), we must call .task_done()
        # to decrement the queue's internal counter.
        q.task_done()

if __name__ == "__main__":
    work_queue = queue.Queue()
    num_consumers = 3
    
    producer_thread = threading.Thread(target=producer, args=(work_queue, num_consumers))
    consumer_threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer, args=(i, work_queue))
        t.start()
        consumer_threads.append(t)

    print("--- Robust Queue Usage Demonstration ---")
    producer_thread.start()
    
    # --- Solution 3: Waiting for completion with queue.join() ---
    # The producer does not need to be joined manually. Instead, the main
    # thread blocks on `work_queue.join()`. This call will only unblock
    # when the queue's internal counter becomes zero, which happens after
    # `task_done()` has been called for every item that was put into it.
    producer_thread.join() # Wait for producer to put all items and pills
    print("[Main] Producer has finished. Waiting for consumers to process all items...")
    work_queue.join()
    
    print("\n[Main] Queue has been fully processed. All consumers should have exited.")
    
    # We don't need to join the consumers here because queue.join() already
    # confirms their work is done, and they will exit. We just verify.
    for t in consumer_threads:
        t.join(timeout=1)

    print("\n--- Results ---")
    alive_consumers = [t.name for t in consumer_threads if t.is_alive()]
    if not alive_consumers:
        print("🟢 SUCCESS: All consumer threads exited cleanly.")