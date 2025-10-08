# /examples/6_implementation_pitfalls/6_7_queue_specific_issues/bad_example.py

import threading
import queue
import time

def producer(q):
    """Produces a few items and then sends a shutdown signal."""
    for i in range(5):
        item = f"Item-{i}"
        print(f"[Producer] Putting '{item}' into the queue.")
        q.put(item)
        time.sleep(0.5)
        
    # --- Mistake 1: Improper Shutdown Signal ---
    # With multiple consumers, a single 'poison pill' is not enough.
    # Only one consumer will receive it and exit, while the others
    # will be stuck waiting on an empty queue forever.
    print("[Producer] Putting a single poison pill (None) into the queue.")
    q.put(None)

def consumer(consumer_id, q):
    """A consumer that processes items from the queue."""
    # --- Mistake 2: Unhandled queue.Empty ---
    # This block demonstrates what happens if you use get_nowait()
    # without proper error handling.
    try:
        # Try to get an item immediately, but the queue is empty at the start.
        item = q.get_nowait() 
        print(f"[Consumer-{consumer_id}] (nowait) Got {item}")
    except queue.Empty:
        # In this script, we catch it, but we show the error.
        # In many real-world cases, this would be an unhandled exception
        # that crashes the worker thread.
        print(f"[Consumer-{consumer_id}] (nowait) Found queue empty, which could crash a worker.")

    # Main processing loop
    while True:
        # q.get() is a blocking call. It will wait here forever if the
        # queue is empty and no more items are added.
        item = q.get()
        if item is None: # The poison pill
            print(f"[Consumer-{consumer_id}] Received poison pill. Exiting.")
            # This break will only be reached by ONE consumer.
            break
        print(f"[Consumer-{consumer_id}] Processing '{item}'...")
        time.sleep(1)

if __name__ == "__main__":
    work_queue = queue.Queue()
    num_consumers = 3
    
    producer_thread = threading.Thread(target=producer, args=(work_queue,))
    consumer_threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer, args=(i, work_queue))
        consumer_threads.append(t)

    print("--- Queue-Specific Issues Demonstration ---")
    
    producer_thread.start()
    for t in consumer_threads:
        t.start()
        
    # We join with a timeout to show that the threads are stuck.
    producer_thread.join()
    for t in consumer_threads:
        t.join(timeout=3)

    print("\n--- Results ---")
    alive_consumers = [t.name for t in consumer_threads if t.is_alive()]
    if alive_consumers:
        print(f"🔴 DEADLOCK: The following consumers are still alive and stuck: {alive_consumers}")
        print("This is because not enough poison pills were sent for shutdown.")