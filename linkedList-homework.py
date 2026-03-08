class Node:
    """Represents a node in a singly linked list."""
    def __init__(self, data=None):
        self.data = data # Data contained within the node
        self.next = None # Reference to the next node
        
    # alternatively: def __init__(self, data = None, next = None):
    
    def __str__(self) -> str:
        """Returns the string representation of the node (for printing)."""
        return str(self.data)

class LinkedList:
    """Represents a singly linked list with a sentinel node at the end (endnode).
    
    The sentinel node does not contain meaningful data and serves as a marker for the end of the list.


    The list supports two types of iterators:
    - LinkedListIterator (Python-style traversal)
    - PositionIterator (STL-like position representation)
    """
    
    def __init__(self):
        """Initializes an empty single linked list with a sentinel node (endnode)."""
        self.end_node = Node()
        self.head = self.end_node

    def is_empty(self) -> bool:
        """Returns True if the linked list is empty (i.e., contains only the sentinel node), False otherwise."""
        if self.head == self.end_node:
            return True
        return False


    def append(self, data):
        """Appends a new node with the given data to the end of the linked list."""
        self.end_node.data = data
        new_node = Node(None)
        self.end_node.next = new_node
        self.end_node = new_node
        return


    def insert_at_beginning(self, data):
        """Inserts a new node with the given data at the beginning of the linked list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        return


    def display(self):
        """Prints the whole linked list."""
        actual_node = self.head

        while actual_node != self.end_node:
            print(actual_node, end = " -> ")
            actual_node = actual_node.next
        print(".")


    def __str__(self) -> str:
        """Converts the LinkedList to string (for print): lists data from all nodes in the linked list."""
        actual_node = self.head
        string = ""

        while actual_node != self.end_node:
            string += str(actual_node) + " -> "
            actual_node = actual_node.next
        return string + " ."


    def delete_all(self):
        """Deletes all nodes from the linked list (except the sentinel node)."""
        actual_node = self.head
        
        while actual_node != self.end_node:
            ref = actual_node.next
            actual_node.data = None
            actual_node = ref
        self.head = self.end_node
        return

    def find(self, data) -> Node:
        """
        Finds the first occurrence of a node with the specified data in the linked list.
        
        Returns:
            - The first node containing the specified data, if found.
            - None if no matching node is found.
        """
        actual_node = self.head

        while actual_node != self.end_node:
            if actual_node.data == data:
                return actual_node
            actual_node = actual_node.next
        return None


    def first(self):
        """
        Returns the data stored in the first node of the linked list.
        
        Raises:
            ValueError: If the linked list is empty.
        """
        if self.head != self.end_node:
            return self.head.data
        raise ValueError("Linked list is empty")


    def last(self):
        """
        Returns the data stored in the last node of the linked list (the node before the sentinel node).
        
        Raises:
            ValueError: If the linked list is empty.
        """
        actual_node = self.head

        if self.head == self.end_node: # if list is empty
            raise ValueError("Linked list is empty")

        while actual_node != self.end_node:
            data = actual_node.data
            actual_node = actual_node.next
        return data


    def remove_first(self):
        """
        Removes the first node of the linked list and returns the data from it.
        
        Raises:
            ValueError: If the linked list is empty.
        """
        if self.head == self.end_node: # if list is empty
            raise ValueError("Linked list is empty")
        
        first_node = self.head
        self.head = first_node.next
        return first_node.data


    def remove_last(self):
        """
        Removes the last node of the linked list and returns the data from it.
        
        Raises:
            ValueError: If the linked list is empty.
        """
        actual_node = self.head

        #* List isn't empty
        if self.head == self.end_node:
            raise ValueError("Linked list is empty")

        #* Next node is end_node
        elif actual_node.next == self.end_node:
            data = actual_node.data
            self.head = self.end_node
            return data

        #* General
        while actual_node.next != self.end_node:
            ref = actual_node
            actual_node = actual_node.next

            if actual_node.next == self.end_node:
                ref.next = self.end_node
                return actual_node.data


    def delete(self, data):
        """
        Deletes the first occurrence of a node with the specified data from the linked list.
        
        Returns:
            bool: True if a node was deleted, False if the data was not found.
        """
        #* Check for empty list
        if self.head == self.end_node:
            return False
        
        #* Data in the first node
        actual_node = self.head
        
        if self.head.data == data:
            self.head = actual_node.next
            return True

        #* General
        while actual_node != self.end_node:
            if actual_node.next != self.end_node and actual_node.next.data == data:
                next_node = actual_node.next
                actual_node.next = next_node.next
                return True

            actual_node = actual_node.next
        return False # node wasn't found


#! Tests
if __name__ == "__main__":
    lst = LinkedList()
    lst.insert_at_beginning("A")
    lst.insert_at_beginning("B")
    lst.insert_at_beginning("C")
    print("Running tests on following list:")
    lst.display()
    print("")

    #* First()
    print(f"first(): {lst.first()}")
    try:
        LinkedList().first()
    except ValueError as e:
        print(f"first() on empty list: {e}")
    print("")

    #* Remove first()
    print(f"remove_first(): {lst.remove_first()}")
    lst.display()
    try:
        LinkedList().remove_first()
    except ValueError as e:
        print(f"remove_first() on empty list: {e}")
    print("")

    #* Last()
    print(f"last(): {lst.last()}")
    try:
        LinkedList().last()
    except ValueError as e:
        print(f"last() on empty list: {e}")
    print("")

    #* Remove last()
    print(f"remove_last(): {lst.remove_last()}")
    lst.display()
    try:
        LinkedList().remove_last()
    except ValueError as e:
        print(f"remove_last() on empty list: {e}")
    print("")

    #* Find()
    print(f"find('B'): {lst.find('B')}")
    print(f"find('D'): {lst.find('D')}\n")

    #* Delete()
    lst.insert_at_beginning("A")
    lst.insert_at_beginning("C")
    print(f"delete('C'): {lst.delete('C')}")
    lst.display()
    print(f"delete('D'): {lst.delete('D')}")