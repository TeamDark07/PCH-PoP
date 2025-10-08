# /examples/5_asyncio_pitfalls/5_4_using_threading_primitives_in_asyncio/good_example.py

import asyncio

# An asynchronous, non-blocking lock from the 'asyncio' module.
shared_lock = asyncio.Lock()
shared_resource = []

async def fast_task():
    """A task that runs concurrently to show the loop is NOT blocked."""
    while True:
        print("(Fast task is running in the background)")
        try:
            await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            break

async def worker(name):
    """
    A worker that correctly uses an asyncio.Lock.
    """
    print(f"[{name}] Attempting to acquire the non-blocking asyncio.Lock...")
    
    # --- The Solution is Here ---
    # `async with shared_lock:` is the correct syntax.
    # If the lock is held, this `await` expression will pause this
    # coroutine and yield control to the event loop, allowing other
    # tasks like `fast_task` to run.
    async with shared_lock:
        print(f"[{name}] Acquired the lock.")
        shared_resource.append(name)
        
        # We also replace the blocking time.sleep() with await asyncio.sleep()
        print(f"[{name}] 'Working' for 2 seconds (while yielding)...")
        await asyncio.sleep(2)
        
        print(f"[{name}] Releasing the lock.")

async def main():
    print("--- Using a Non-Blocking `asyncio.Lock` ---")

    fast_task_handle = asyncio.create_task(fast_task())
    await asyncio.sleep(0.1)
    
    # Start the two workers.
    await asyncio.gather(
        worker("Worker-A"),
        worker("Worker-B"),
    )
    
    print("\nObserve the output: The 'Fast task' NEVER stopped running,")
    print("even when a worker was 'waiting' for or 'holding' the lock.")

    # Cleanly stop the background task.
    fast_task_handle.cancel()

if __name__ == "__main__":
    asyncio.run(main())