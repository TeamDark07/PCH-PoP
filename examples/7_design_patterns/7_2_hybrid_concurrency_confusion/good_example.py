# /examples/7_design_patterns/7_2_hybrid_concurrency_confusion/good_example.py

import threading
import asyncio
import time

async def async_worker(item):
    """A simple coroutine that does some async work."""
    print(f"[Asyncio] Received item '{item}', working...")
    await asyncio.sleep(1)
    print(f"[Asyncio] Finished work for '{item}'.")
    return f"Result for {item}"

def run_asyncio_loop_in_thread(loop):
    """Function to set up and run the event loop in a background thread."""
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()

def external_thread_submitter(loop):
    """
    An external thread that safely submits work to the asyncio loop.
    """
    items_to_submit = ["A", "B", "C"]
    futures = []
    
    for item in items_to_submit:
        print(f"[External Thread] Safely submitting item '{item}' to the loop...")
        
        # --- The Solution: `loop.call_soon_threadsafe()` ---
        # This function is the ONLY safe way to schedule a callback or coroutine
        # on an event loop that is running in a different thread. It uses a
        # thread-safe mechanism to wake up the event loop and add the item.
        # It can even return a Future-like object to get results back.
        future = asyncio.run_coroutine_threadsafe(async_worker(item), loop)
        futures.append((item, future))
        
        time.sleep(0.5)

    # Now, wait for the results in the synchronous thread.
    for item, future in futures:
        result = future.result() # This blocks until the coroutine is done.
        print(f"[External Thread] Got result for '{item}': '{result}'")

    # Safely stop the loop.
    loop.call_soon_threadsafe(loop.stop)

if __name__ == "__main__":
    print("--- Correct Hybrid Concurrency (Thread-Safe Interaction) ---")
    
    asyncio_loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=run_asyncio_loop_in_thread, args=(asyncio_loop,))
    loop_thread.start()
    time.sleep(1)
    
    external_thread = threading.Thread(target=external_thread_submitter, args=(asyncio_loop,))
    external_thread.start()
    
    external_thread.join()
    loop_thread.join()
    
    print("\nProgram finished. The interaction was thread-safe and robust.")