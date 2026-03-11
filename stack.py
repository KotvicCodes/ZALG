class Stack:
    """Class representing a stack (LIFO) implemented using a linked list."""
    
    def __init__(self):
        """Initializes an empty stack."""
        self.lst = []
        self.count = 0
    
    def is_empty(self):
        """Returns True if the stack is empty, otherwise False."""
        return self.lst == []
    
    def __len__(self):
        """Returns the number of elements in the stack."""
        return len(self.lst)
    
    def push(self, data):
        """Adds an element to the top of the stack."""
        return self.lst.append(data)
    
    def pop(self):
        """Removes the top element of the stack and returns data from it.
        Raises an error if the stack is empty.
        """
        if self.is_empty():
            raise ValueError("The list is empty")
        return self.lst.pop()
    
    def top(self):
        """Returns data from the top element of the stack without removing it.
        Raises an error if the stack is empty.
        """
        return 

class Queue:
    """Class representing a queue (FIFO) implemented using a linked list."""
    
    def __init__(self):
        """Initializes an empty queue."""
        ...
    
    def is_empty(self):
        """Returns True if the queue is empty, otherwise False."""
        ...
    
    def __len__(self):
        """Returns the number of elements in the queue."""
        ...
    
    def enqueue(self, data): 
        """Adds an element to the end of the queue."""
        ...
    
    def dequeue(self):
        """Removes the front element of the queue and returns data from it.
        Raises an error if the queue is empty.
        """
        ...
    
    def front(self):
        """Returns data from the front element of the queue without removing it.
        Raises an error if the queue is empty.
        """
        ...




def test_stack():
    s = Stack()
    
    print("start:", len(s), s.is_empty())

    for x in range(10):
        s.push(x)
    
    print("after push:", len(s), s.is_empty())
    
    while not s.is_empty():
        print(s.top(), s.pop())

    print("end:", len(s), s.is_empty())

if __name__ == "__main__":
    ...
    # test_stack()