class Node:
    """Represents a node in a binary search tree."""

    def __init__(self, data=None):
        self.data = data    # Data contained within the node
        self.left = None    # Reference to the left child Node
        self.right = None   # Reference to the right child Node

    def __str__(self) -> str:
        """Return string representation of the node."""
        return str(self.data)

class BinarySearchTree:
    """
    Represents a Binary Search Tree.
    
    For every node:
    left subtree values < node.data < right subtree values
    """

    def __init__(self):
        """Initializes an empty binary search tree."""
        self.root = None   # Reference to the root node


    def is_empty(self) -> bool:
        """Returns True if the BST is empty, False otherwise."""
        return self.root == None


    def find(self, data):
        """
        Search for a node with the given data. Implement without recursion.

        Parameters:
            data: Data to search for.

        Returns:
            Node with the given data if found, otherwise None.
        """
        current_node = self.root
        if self.is_empty():
            return None

        while True:
            if data < current_node.data:
                current_node = current_node.left
            elif data > current_node.data:
                current_node = current_node.right

            if current_node == None:
                return None
            elif data == current_node.data:
                return current_node
    

    def recursive_find(self, data, current_node=None, firstCall=True):
        """
        Search for a node with the given data. Implement with recursion.

        Parameters:
            data: Data to search for.

        Returns:
            Node with the given data if found, otherwise None.
        """    
        # check for first call
        if firstCall:
            current_node = self.root

        # check for none
        if current_node == None:
            return None
        
        # initial condition
        if current_node.data == data:
            return current_node
        
        # call recursion with proper new node
        elif data > current_node.data:
            return self.recursive_find(data, current_node.right, False)
        elif data < current_node.data:
            return self.recursive_find(data, current_node.left, False)


    def insert(self, data) -> None:
        """
        Insert a new node into the BST. If a node with the given data already exists, 
        do nothing. Implement without/with recursion.

        Parameters:
            data: Data to store in the BST.
        """
        if self.root is None:
            self.root = Node(data)
            return
        actual_node = self.root
        while actual_node is not None:
            if actual_node.data == data:
                return
            elif actual_node.data > data:
                if actual_node.left is None:
                    actual_node.left = Node(data)
                    return
                actual_node = actual_node.left
            else:# actual_node.data <  data
                if actual_node.right is None:
                    actual_node.right = Node(data)
                    return
                actual_node = actual_node.right

    def print_inorder(self) -> None:
        """
        Print all elements in the BST in ascending order (inorder traversal).

        Example output: 2, 8, 10
        """
        ...

    def print_structure(self) -> None:
        """
        Print the BST structure (each node on a separate line)
        with indentation reflecting tree depth.

        The traversal order (preorder, inorder, or postorder) is optional.

        Example output (for inorder traversal):

                4
            6
        7
                10
            18
                24
        """
        ...

    def delete_all(self) -> None:
        """
        Delete all nodes in the BST.

        Implement using recursion (postorder traversal) and the del statement.
        """
        ...

    def copy(self) -> "BinarySearchTree":
        """
        Return a deep copy of the BST.

        Implement using recursion.

        Returns:
            A new BinarySearchTree containing copies of all nodes.
        """
        ...

    def delete(self, data) -> None:
        """
        Delete a node with the given data if it exists.

        Parameters:
            data: Data of the node to delete.
        """
        ...

    def count(self) -> int:
        """
        Return the number of nodes in the BST.

        Implement using recursion.
        """
        ...

    def depth(self) -> int:
        """
        Return the depth of the BST.

        Implement using recursion.

        Returns:
            Depth (height) of the tree.
        """
        ...

    def find_min(self):
        """
        Find and return the node with the smallest data in the BST.

        Implement without recursion.

        Returns:
            Node with the smallest data, or None for an empty BST.
        """
        ...

    def serialize_to_list(self) -> list:
        """
        Preorder serialization: convert the BST to a list representation
        using preorder traversal.

        Returns:
            A list of data values stored in the BST.
        """
        ...

    @staticmethod
    def reconstruct_from_list(input_list: list) -> "BinarySearchTree":
        """
        Deserialize a BST from the list representation produced
        by serialize_to_list().

        The internal structure of the reconstructed tree must be
        the same as the original one.

        Parameters:
            input_list: List produced by serialize_to_list().

        Returns:
            Reconstructed BinarySearchTree.
        """
        ...

    #########################################################

    def print_by_levels_recursive(self) -> None:
        """
        Print nodes level by level (level-order traversal).
        Nodes at the same depth are printed on the same line.

        Implement breadth-first traversal using recursive
        depth-first traversal.

        BONUS: Indent output to reflect tree structure.

        Example output:

               7
          3       16
        1   6      25
        """
        ...

    def print_by_levels_queue(self) -> None:
        """
        Print BST data by levels (each level on a separate line)
        using a queue.

        Implement breadth-first traversal non-recursively.

        Use the Queue class from a previous assignment.

        BONUS: Indent output to reflect tree structure.
        """
        ...

    def print_preorder_stack(self) -> None:
        """
        Print BST nodes in preorder (each node on a new line).

        Implement depth-first traversal using a stack.

        Use the Stack class from a previous assignment.

        BONUS: Indent output based on tree depth.
        """
        ...

    #########################################################

    @staticmethod
    def from_ordered_list(input_list: list) -> "BinarySearchTree":
        """
        Construct a balanced BST from a sorted list.

        Time complexity: O(n).

        Parameters:
            input_list: List of data sorted in ascending order.

        Returns:
            A balanced BinarySearchTree containing the elements.
        """
        ...


if __name__ == "__main__":
    tree = BinarySearchTree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(10)
    tree.insert(1)
    tree.insert(25)
    tree.insert(35)

    print(tree.find(35))
    print(tree.find(99))
    print(tree.recursive_find(3))
    print(tree.recursive_find(99))