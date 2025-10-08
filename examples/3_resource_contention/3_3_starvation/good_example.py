# /examples/3_resource_contention/3_3_starvation/good_example.py

import threading
import time
import random
from collections import deque

# A Condition variable provides both a lock and a way to wait for events.
# We will use it to build a fair lock.
fair_condition = threading.Condition()
stop_event = threading.Event()

# A queue to manage which thread is next in line.
waiting_queue = deque()
resource_in_use = False

def fair_worker(worker_id, is_patient=False):
    """
    A worker that uses a fair, queue-based locking mechanism.
    """
    global resource_in_use
    my_turn_event = threading.Event()

    with fair_condition:
        # Each thread adds itself to the queue.
        waiting_queue.append((worker_id, my_turn_event))
        print(f"[{worker_id}] is now in line.")

    # Wait for our turn.
    my_turn_event.wait()

    # --- At this point, it's our turn to use the resource ---
    print(f"[{worker_id}] It's my turn! Using the resource.")
    if is_patient:
        time.sleep(0.1) # Patient worker does its thing
    else:
        time.sleep(0.01) # Greedy worker does its thing
    
    # Signal that we are done.
    with fair_condition:
        resource_in_use = False
        # Wake up the scheduler to let the next person in line go.
        fair_condition.notify()

def scheduler():
    """
    A central scheduler that ensures fairness by granting access
    in the order threads arrived in the queue.
    """
    global resource_in_use
    while not stop_event.is_set() or waiting_queue:
        with fair_condition:
            # Wait until there's someone in line AND the resource is free.
            while not waiting_queue or resource_in_use:
                fair_condition.wait(timeout=0.1)
                if stop_event.is_set() and not waiting_queue: 
                    return
            
            # Get the next thread in line.
            worker_id, turn_event = waiting_queue.popleft()
            resource_in_use = True
            
            # Signal that it's their turn.
            turn_event.set()

if __name__ == "__main__":
    NUM_GREEDY_WORKERS = 5
    
    print("--- Starvation Avoidance with a Fair Queue ---")
    
    # Start the scheduler thread first
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.start()
    
    # Start the workers
    threads = []
    for i in range(NUM_GREEDY_WORKERS):
        threads.append(threading.Thread(target=fair_worker, args=(f"Greedy-{i}",)))
    
    # The patient worker gets in line like everyone else.
    threads.append(threading.Thread(target=fair_worker, args=("Patient", True)))
    
    random.shuffle(threads) # Shuffle to make the start order random
    for t in threads:
        t.start()
        time.sleep(0.01)

    for t in threads:
        t.join()
        
    stop_event.set()
    scheduler_thread.join()
    
    print("\nSimulation finished. All workers got their turn.")