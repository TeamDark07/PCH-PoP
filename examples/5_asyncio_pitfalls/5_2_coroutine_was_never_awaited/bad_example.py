# /examples/5_asyncio_pitfalls/5_2_coroutine_was_never_awaited/bad_example.py

import asyncio

# A coroutine function defined with 'async def'.
# Calling this function does NOT run it. It returns a coroutine object.
async def important_task():
    """Simulates an important task that needs to be run."""
    print("Starting the important task...")
    await asyncio.sleep(1) # Simulate I/O work
    print("Important task has finished!")

async def main():
    print("--- 'Coroutine Was Never Awaited' Demonstration ---")
    
    print("Calling 'important_task()' without 'await'...")
    
    # --- The Mistake is Here ---
    # We are calling the async function like a regular function.
    # This creates a coroutine object, but does nothing with it.
    # The event loop is never told to run this coroutine.
    result = important_task()
    
    print(f"The return value of the call is: {result}")
    print("Notice that the task's print statements did NOT appear.")
    
    # The program will now finish without the task ever running.
    # Python will likely print a 'RuntimeWarning' when the program exits
    # because the coroutine object was created but never awaited.

if __name__ == "__main__":
    asyncio.run(main())
    
    # A small sleep to ensure the warning has time to be printed upon exit.
    import time
    time.sleep(0.1)