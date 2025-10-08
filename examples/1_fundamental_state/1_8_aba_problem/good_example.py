# /examples/1_fundamental_state/1_8_aba_problem/good_example.py

import threading

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class VersionedReference:
    """A container for a value and a version counter."""
    def __init__(self, value, version=0):
        self.value = value
        self.version = version

# The head is now a versioned reference
head_ref = None

# Events for choreography
t1_read_head = threading.Event()
t2_interfered = threading.Event()

def compare_and_swap(ref, expected_value, expected_version, new_value):
    """
    Simulated Compare-And-Swap that also checks the version.
    In a real system, this would be a single atomic hardware instruction.
    """
    if ref.value == expected_value and ref.version == expected_version:
        ref.value = new_value
        ref.version += 1 # Increment version on every successful swap
        return True
    return False

def thread1_pop_A():
    """
    Thread 1 tries to pop Node A, but its CAS will fail due to the
    version mismatch, correctly preventing corruption.
    """
    # 1. Read the head and its version.
    local_head_value = head_ref.value
    local_head_version = head_ref.version
    next_node = local_head_value.next
    print(f"Thread 1: Read head '{local_head_value.value}' (v{local_head_version}). Next is '{next_node.value}'.")
    
    t1_read_head.set()
    print("Thread 1: Pausing, allowing interference...")
    t2_interfered.wait()
    print("Thread 1: Resuming.")

    # 2. Perform the version-aware CAS.
    if compare_and_swap(head_ref, local_head_value, local_head_version, next_node):
        print(f"Thread 1: CAS successful. New head is '{head_ref.value.value}'.")
    else:
        print(f"Thread 1: CAS failed! Current version is {head_ref.version}, expected {local_head_version}.")
        print("Thread 1: Would need to retry the whole operation.")

def thread2_interfere():
    """
    Thread 2 interferes, but each modification increments the version counter.
    """
    t1_read_head.wait()
    print("Thread 2: Starting interference.")
    
    # Pop A
    popped_A = head_ref.value
    compare_and_swap(head_ref, popped_A, 0, popped_A.next) # v0 -> v1
    print(f"Thread 2: Popped '{popped_A.value}', head is now '{head_ref.value.value}' (v{head_ref.version}).")
    
    # Pop C
    popped_C = head_ref.value
    compare_and_swap(head_ref, popped_C, 1, popped_C.next) # v1 -> v2
    print(f"Thread 2: Popped '{popped_C.value}', head is now '{head_ref.value.value}' (v{head_ref.version}).")

    # Push A back
    popped_A.next = head_ref.value
    compare_and_swap(head_ref, head_ref.value, 2, popped_A) # v2 -> v3
    print(f"Thread 2: Pushed '{popped_A.value}' back, head is now '{head_ref.value.value}' (v{head_ref.version}).")

    t2_interfered.set()

def print_stack(start_node):
    nodes = []
    curr = start_node
    while curr:
        nodes.append(curr.value)
        curr = curr.next
    print("Final stack state:", " -> ".join(nodes))

if __name__ == "__main__":
    node_B = Node("B")
    node_C = Node("C", node_B)
    node_A = Node("A", node_C)
    head_ref = VersionedReference(node_A, 0)
    
    t1 = threading.Thread(target=thread1_pop_A)
    t2 = threading.Thread(target=thread2_interfere)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n--- ABA Problem Solved ---")
    print_stack(head_ref.value)
    print("The stack is not corrupted because the version check prevented the invalid update.")