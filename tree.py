class Node:
    def __init__(self, value, trail):
        self.value = value  # Sorting value
        self.trail = trail  # Corresponding trail
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value, trail):
        # Insert value and trail
        if self.root is None:
            self.root = Node(value, trail)
        else:
            self._insert(value, trail, self.root)

    def _insert(self, value, trail, node):
        # Helper for insert
        if value < node.value:
            if node.left is None:
                node.left = Node(value, trail)
            else:
                self._insert(value, trail, node.left)
        else:
            if node.right is None:
                node.right = Node(value, trail)
            else:
                self._insert(value, trail, node.right)

    def find_max(self):
        # Find max value
        if self.root is None:
            return None
        current_node = self.root
        while current_node.right:
            current_node = current_node.right
        return current_node.value

    def find_min(self):
        # Find min value
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.value

    def inorder_traversal(self, node, result=None):
        # Inorder traversal (ascending)
        if result is None:
            result = []
        if node:
            self.inorder_traversal(node.left, result)
            result.append((node.value, node.trail))  # Value and trail
            self.inorder_traversal(node.right, result)
        return result

    def sortmintomax(self):
        # Sort min to max
        if self.root:
            return self.inorder_traversal(self.root)

    def sort_max_to_min(self):
        # Sort max to min
        result = []
        self._reverse_in_order_traversal(self.root, result)
        return result

    def _reverse_in_order_traversal(self, node, result):
        # Helper for reverse in-order
        if node:
            self._reverse_in_order_traversal(node.right, result)
            result.append((node.value, node.trail))  # Value and trail
            self._reverse_in_order_traversal(node.left, result)
