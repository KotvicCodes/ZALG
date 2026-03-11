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

    def delete_all_occurrences(self, data):
        """
        Deletes all nodes with the specified data from the linked list.
        
        Returns:
            int: The number of deleted nodes.
        """
        #? opt1: self.head = self.end_node # máme garbage collector
        #* Opt: 2
        while self.head != self.end_node:
            actual = self.head
            self.head = actual.next
            del actual
            # actual.next = None

    def __getitem__(self, index: int):
        """
        Returns the data stored at the specified index (0-based).
        
        Raises:
            IndexError: If the index is out of range.
        """
        ...

    def __setitem__(self, index: int, data):
        """
        Sets the data at the specified index (0-based).
        
        Raises:
            IndexError: If the index is out of range.
        """
        ...

    def __iter__(self):
        """
        Returns a Python iterator for the linked list.
        """
        ...
    
    def find_iter(self, data) -> "PositionIterator":
        """
        Returns an iterator pointing to the first occurrence of the specified data.
        """
        ...

    def start_iter(self) -> "PositionIterator":
        """
        Returns an iterator pointing to the first element of the list.
        """
        ...
    
    def end_iter(self) -> "PositionIterator":
        """
        Returns an iterator pointing to the sentinel node (endnode).
        """
        ...
    
class LinkedListIterator:
    """
    Python-style iterator for the LinkedList class.

    This iterator follows the Python iterator protocol and is used in for-loops
    """

    def __init__(self, head: Node, endnode: Node):
       """
       Initializes the iterator with the starting node and the sentinel node (endnode) marking the end of the list.
       """        
       ...
    
    def __iter__(self):
        """ Returns the iterator object itself (required by the iterator protocol)."""
        ...

    def __next__(self):
        """
        Returns the next data element in the list.
        
        Raises:
            StopIteration: If the iterator reaches the sentinel node (endnode).
        """
        ...


class PositionIterator:
    """Custom STL-like iterator representing a position inside the linked list."""
    def __init__(self, linked_list, node: Node):
        """
        Initializes the iterator with a reference to the linked list and a node representing the current position.
        """
        ...

    def __eq__(self, __value: object):
        """Checks whether two iterators represent the same position."""
        ...
    
    def get_value(self):
        """Returns the value stored at the current iterator position.
           
           Raises:
               ValueError: If the iterator points to the sentinel node (endnode).
        """
        ...
    
    def set_value(self, data):
        """Sets the value at the current iterator position.
        
           Raises:
               ValueError: If the iterator points to the sentinel node (endnode).
        """
        ...
    
    def move_to_next(self):
        """Moves the iterator to the next position in the linked list.
        
        Raises:
               ValueError: If the iterator points to the sentinel node (endnode).
        """
        ...


if __name__ == "__main__":
    node = Node("A")
    # print(node)
    lst = LinkedList()
    lst.insert_at_beginning("A")
    lst.insert_at_beginning("B")
    lst.insert_at_beginning("C")
    lst.display()
    print(lst.remove_last())
    lst.display()
    

def test():
    n = Node("John")
    print(n)

    l = LinkedList()
    for i in range(10):
        l.append(i)
    print(l)

    # Indexation ... setitem, getitem
    """
    print(l[1])
    l[1] = 12
    print(l)
    """
    
    # Python iterator:
    '''
    for x in l:
        print(x)
    '''

    # Position iterator (STL-like usage):
    '''
    it = l.start_iter()
    end = l.end_iter()

    while it != end:
        print(it.get_value())
        # it.set_value(it.get_value() * 2)
        it.move_to_next()
    '''

