# /examples/5_asyncio_pitfalls/5_1_blocking_the_event_loop/bad_example.py

import asyncio
import time

async def fast_task():
    """A coroutine that should run frequently."""
    while True:
        print("Fast task is running...")
        # Use asyncio.sleep() to yield control to the event loop.
        await asyncio.sleep(1)

async def slow_blocking_task():
    """
    A coroutine that contains a synchronous, blocking call.
    This is the source of the problem.
    """
    print("Slow task started, will block the event loop for 5 seconds.")
    
    # --- The Problem is Here ---
    # time.sleep() is a synchronous, blocking call. It tells the OS to
    # pause the entire thread. Since the asyncio event loop runs in a
    # single thread, this call freezes everything. No other coroutine
    # can run until this sleep is over.
    time.sleep(5)
    
    print("Slow task finished blocking.")

async def main():
    """The main entry point for the asyncio application."""
    print("--- Blocking the Event Loop Demonstration ---")
    
    # Start the fast task to run in the background.
    asyncio.create_task(fast_task())
    
    # Give the fast task a moment to start running.
    await asyncio.sleep(0.1)
    
    # Now, run the slow, blocking task.
    await slow_blocking_task()
    
    print("\nObserve the output:")
    print("The 'Fast task is running...' message stopped appearing for 5 seconds.")
    print("This is because the entire event loop was blocked.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program exited.")