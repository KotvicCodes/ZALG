#

from linkedList import LinkedList, Node

class Stack:
    """Class representing a stack (LIFO) implemented using a linked list."""
    
    def __init__(self):
        """Initializes an empty stack."""
        self.lst = LinkedList()
        self.count = 0
    

    def is_empty(self):
        """Returns True if the stack is empty, otherwise False."""
        return self.lst.is_empty()
    

    def __len__(self):
        """Returns the number of elements in the stack."""
        return self.count
    

    def push(self, data):
        """Adds an element to the top of the stack."""
        self.count += 1
        self.lst.append(data)
        return 
    

    def pop(self):
        """Removes the top element of the stack and returns data from it.
        Raises an error if the stack is empty.
        """
        if self.is_empty():
            raise ValueError("The stack is empty")
        self.count -= 1
        return self.lst.remove_last()
    

    def top(self):
        """Returns data from the top element of the stack without removing it.
        Raises an error if the stack is empty.
        """
        if self.is_empty():
            raise ValueError("The stack is empty")
        return self.lst.last()


class Queue:
    """Class representing a queue (FIFO) implemented using a linked list."""
    
    def __init__(self):
        """Initializes an empty queue."""
        self.lst = LinkedList()
        self.count = 0
    

    def is_empty(self):
        """Returns True if the queue is empty, otherwise False."""
        return self.lst.is_empty()
    

    def __len__(self):
        """Returns the number of elements in the queue."""
        return self.count
    

    def enqueue(self, data): 
        """Adds an element to the end of the queue."""
        self.lst.append(data)
        self.count += 1
        return
    

    def dequeue(self):
        """Removes the front element of the queue and returns data from it.
        Raises an error if the queue is empty.
        """
        if self.is_empty():
            raise ValueError("The queue is empty")
        self.count -= 1
        return self.lst.remove_first()

    
    def front(self):
        """Returns data from the front element of the queue without removing it.
        Raises an error if the queue is empty.
        """
        if self.is_empty():
            raise ValueError("The queue is empty")
        return self.lst.first()


def test_stack():
    s = Stack()
    
    print("start:", len(s), s.is_empty())

    for x in range(10):
        s.push(x)
    
    print("after push:", len(s), s.is_empty())
    
    while not s.is_empty():
        print(s.top(), s.pop())

    print("end:", len(s), s.is_empty())


def test_queue():
    q = Queue()
    
    print("start:", len(q), q.is_empty())

    for x in range(10):
        q.enqueue(x)
    
    print("after push:", len(q), q.is_empty())
    
    while not q.is_empty():
        print(q.front(), q.dequeue())

    print("end:", len(q), q.is_empty())

    try:
        q.dequeue()
    except ValueError as e:
        print(e)

test_stack()
test_queue()