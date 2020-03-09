import numpy as np


class Node:
    def __init__(self, value=0):
        if not isinstance(value, int):
            raise ValueError("Nodes can store only ints")

        self.value = value
        self._parent = None
        self._left = None  # left child
        self._right = None  # right child

    @property
    def parent(self):
        return self._parent

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, other):
        if not isinstance(other, Node):
            raise ValueError("other must be a Node instance")

        self._left = other
        other._parent = self

    @right.setter
    def right(self, other):
        if not isinstance(other, Node):
            raise ValueError("other must be a Node instance")

        self._right = other
        other._parent = self


class BinaryTree:
    def __init__(self, root):
        self.root = root

    @staticmethod
    def _sum(node):
        """ Used internally to compute the sum of the stored values. """
        if node:
            return node.value + BinaryTree._sum(node.left) + BinaryTree._sum(node.right)

        return 0

    @staticmethod
    def _extract_values(node, values):
        """ Used internally to append the stored values to a provided list. """
        if node:
            values.append(node.value)
            BinaryTree._extract_values(node.left, values)
            BinaryTree._extract_values(node.right, values)

    def _validate(self, node):
        """ Used internally to check whether a given node belongs to the tree. """
        while node.parent:
            node = node.parent

        if node is not self.root:
            raise ValueError("node is not a member of this tree")

    def sum(self, node=None):
        """ Returns the sum of the stored values. 
            If node is given, returns the sum of the values stored in a subtree
            whose root is node. """
        if node:
            self._validate(node)
        else:
            node = self.root

        return BinaryTree._sum(node)

    def mean(self, node=None):
        """ Returns the average of the stored values. 
            If node is given, returns the average of the values stored in a subtree
            whose root is node. """
        if node:
            self._validate(node)
        else:
            node = self.root

        values = []
        BinaryTree._extract_values(node, values)
        return np.mean(values)

    def median(self, node=None):
        """ Returns the median of the stored values. 
            If node is given, returns the median of the values stored in a subtree
            whose root is node. """
        if node:
            self._validate(node)
        else:
            node = self.root

        values = []
        BinaryTree._extract_values(node, values)
        return np.median(values)

