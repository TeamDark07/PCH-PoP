# /examples/1_fundamental_state/1_8_aba_problem/bad_example.py

import threading

# A simple node for our linked-list stack
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

# --- A Note on This Example ---
# The ABA problem occurs in lock-free algorithms using a Compare-And-Swap (CAS)
# operation. Since Python doesn't have a native atomic CAS, we simulate it.
# We use Events to deterministically force the ABA sequence to occur.

# Shared "head" of our stack
head = None

# Events to choreograph the threads
t1_read_head = threading.Event()
t2_interfered = threading.Event()

def thread1_pop_A():
    """
    Thread 1 tries to pop Node A, but will be tricked by the ABA problem.
    """
    global head
    
    # 1. Read the head pointer. It points to Node A.
    local_head = head
    next_node = local_head.next
    print(f"Thread 1: Read head, points to '{local_head.value}'. Next is '{next_node.value}'.")
    
    # Signal that we have read the head, allowing Thread 2 to interfere.
    t1_read_head.set()
    
    # Wait for Thread 2 to finish its A -> B -> A modification.
    print("Thread 1: Pausing, allowing interference...")
    t2_interfered.wait()
    print("Thread 1: Resuming.")

    # 2. Perform the "Compare-And-Swap" (CAS).
    # It checks if `head` is still the same as `local_head` (Node A).
    # To Thread 1, it looks like nothing has changed.
    if head == local_head:
        # This is the incorrect action!
        # `head` is now set to `next_node` (Node C), which is now an
        # invalid pointer, orphaning Node B.
        head = next_node
        print(f"Thread 1: CAS successful (incorrectly!). New head is '{head.value}'.")
    else:
        print("Thread 1: CAS failed. Head was modified.")

def thread2_interfere():
    """
    Thread 2 interferes by popping A, popping C, then pushing A back on.
    This creates the A -> B -> A sequence for the `head` pointer.
    """
    global head
    
    # Wait until Thread 1 has read the initial head.
    t1_read_head.wait()
    print("Thread 2: Starting interference.")
    
    # Pop A (head now points to C)
    popped_A = head
    head = head.next
    print(f"Thread 2: Popped '{popped_A.value}', head is now '{head.value}'.")

    # Pop C (head now points to B)
    popped_C = head
    head = head.next
    print(f"Thread 2: Popped '{popped_C.value}', head is now '{head.value}'.")
    
    # Push A back onto the stack. `head` now points to A again.
    # However, the stack's structure is completely different.
    popped_A.next = head
    head = popped_A
    print(f"Thread 2: Pushed '{popped_A.value}' back, head is now '{head.value}'.")

    # Signal that the interference is complete.
    t2_interfered.set()


def print_stack(start_node):
    """Utility to print the final state of the stack."""
    nodes = []
    curr = start_node
    while curr:
        nodes.append(curr.value)
        curr = curr.next
    print("Final stack state:", " -> ".join(nodes))


if __name__ == "__main__":
    # Initial stack: A -> C -> B
    node_B = Node("B")
    node_C = Node("C", node_B)
    head = Node("A", node_C)
    
    t1 = threading.Thread(target=thread1_pop_A)
    t2 = threading.Thread(target=thread2_interfere)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n--- ABA Problem Result ---")
    print_stack(head)
    print("The stack is corrupted. Node B has been orphaned/lost.")