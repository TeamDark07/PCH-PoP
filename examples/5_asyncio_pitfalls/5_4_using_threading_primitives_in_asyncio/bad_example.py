# /examples/5_asyncio_pitfalls/5_4_using_threading_primitives_in_asyncio/bad_example.py

import asyncio
import threading
import time

# A standard, blocking lock from the 'threading' module.
shared_lock = threading.Lock()
shared_resource = []

async def fast_task():
    """A task that should run concurrently to show if the loop is blocked."""
    while True:
        print("(Fast task is running in the background)")
        await asyncio.sleep(0.5)

async def worker(name):
    """
    A worker coroutine that tries to use a threading.Lock to protect a resource.
    """
    print(f"[{name}] Attempting to acquire the blocking threading.Lock...")
    
    # --- The Problem is Here ---
    # `shared_lock.acquire()` is a blocking call. If the lock is held,
    # it pauses the entire thread, which freezes the asyncio event loop.
    # No other coroutine, including `fast_task`, can run.
    with shared_lock:
        print(f"[{name}] Acquired the lock.")
        shared_resource.append(name)
        
        # Simulate holding the lock for some I/O or work
        print(f"[{name}] Holding lock for 2 seconds...")
        time.sleep(2) # This is also a blocking call!
        
        print(f"[{name}] Releasing the lock.")

async def main():
    print("--- Using a Blocking `threading.Lock` in `asyncio` ---")
    
    # Start the background task so we can see when the loop is blocked.
    asyncio.create_task(fast_task())
    await asyncio.sleep(0.1)

    # Start two workers that will compete for the blocking lock.
    await asyncio.gather(
        worker("Worker-A"),
        worker("Worker-B"),
    )
    
    print("\nObserve the output: The 'Fast task' stopped running whenever")
    print("a worker was holding the blocking lock.")

if __name__ == "__main__":
    # Add a timeout to stop the program, as fast_task runs forever.
    try:
        asyncio.run(asyncio.wait_for(main(), timeout=5.0))
    except asyncio.TimeoutError:
        print("\nProgram finished.")