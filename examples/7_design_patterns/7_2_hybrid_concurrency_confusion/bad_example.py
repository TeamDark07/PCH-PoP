# /examples/7_design_patterns/7_2_hybrid_concurrency_confusion/bad_example.py

import threading
import asyncio
import time

# --- A Note on This Example ---
# The failure mode of this anti-pattern can be subtle. It might seem to work
# sometimes, but it is a race condition and not guaranteed to be safe.
# It can lead to unpredictable behavior or crashes in complex applications.

async def async_worker(item):
    """A simple coroutine that does some async work."""
    print(f"[Asyncio] Received item '{item}', working...")
    await asyncio.sleep(1)
    print(f"[Asyncio] Finished work for '{item}'.")

def run_asyncio_loop_in_thread(loop):
    """Function to set up and run the event loop in a background thread."""
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()

def external_thread_submitter(loop):
    """

    An external, synchronous thread that tries to submit work to the
    running asyncio loop.
    """
    items_to_submit = ["A", "B", "C"]
    for item in items_to_submit:
        print(f"[External Thread] Submitting item '{item}' to the loop...")
        
        # --- The Problem: Not Thread-Safe ---
        # `loop.call_soon()` is NOT thread-safe. Calling it from an
        # external thread can corrupt the internal state of the event loop.
        # While it may appear to work in this simple case, it is an
        # unsafe race condition.
        loop.call_soon(asyncio.create_task, async_worker(item))
        
        time.sleep(0.5) # Simulate doing other work

    # We need a way to stop the loop from the external thread.
    # This is also not ideal, but necessary for the demo.
    loop.call_soon(loop.stop)

if __name__ == "__main__":
    print("--- Hybrid Concurrency Confusion Demonstration ---")
    print("An external thread is submitting work to an asyncio loop unsafely.")
    
    # Create a new event loop that will run in the background.
    asyncio_loop = asyncio.new_event_loop()
    
    # Start the asyncio event loop in a separate thread.
    loop_thread = threading.Thread(target=run_asyncio_loop_in_thread, args=(asyncio_loop,))
    loop_thread.start()
    
    # Give the loop a moment to start up.
    time.sleep(1)
    
    # Start the external thread that will interact with the loop.
    external_thread = threading.Thread(target=external_thread_submitter, args=(asyncio_loop,))
    external_thread.start()
    
    external_thread.join()
    loop_thread.join()
    
    print("\nProgram finished. While it may have appeared to work, the interaction was unsafe.")