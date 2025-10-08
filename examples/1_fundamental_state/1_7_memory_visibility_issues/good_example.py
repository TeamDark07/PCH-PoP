# /examples/1_fundamental_state/1_7_memory_visibility_issues/good_example.py

import threading
import time

# A threading.Event is the correct, safe, and efficient way to signal
# between threads.
done_event = threading.Event()

def worker():
    """
    A worker thread that efficiently waits for a signal using an Event.
    """
    print("Worker starting, waiting for the event...")
    
    # The event.wait() method does two crucial things:
    # 1. It blocks the thread efficiently without consuming CPU.
    # 2. It guarantees proper memory synchronization. When wait() returns,
    #    this thread is guaranteed to see all memory writes made by the
    #    thread that called event.set().
    done_event.wait()
        
    print("Worker received the event and is finishing.")


if __name__ == "__main__":
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    print("Main thread sleeping for 2 seconds...")
    time.sleep(2)

    print("Main thread setting the event.")
    # The event.set() method creates a memory barrier, ensuring that the
    # change in the event's state is visible to all other threads.
    done_event.set()

    # The join() will now reliably complete without a timeout.
    worker_thread.join()

    print("\nWorker thread finished correctly and reliably.")