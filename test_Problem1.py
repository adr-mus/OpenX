import unittest

from Problem1 import Node, BinaryTree


class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.n1, self.n2 = Node(0), Node(0)

    def test_init(self):
        self.assertRaises(ValueError, Node, "1")
        self.assertRaises(ValueError, Node, 1.0)
        self.assertRaises(ValueError, Node, 1 + 2j)

    def test_left_setter(self):
        with self.assertRaises(ValueError):
            self.n1.left = 1
        self.n1.left = self.n2
        self.assertIs(self.n2.parent, self.n1)

    def test_right_setter(self):
        with self.assertRaises(ValueError):
            self.n1.right = 1
        self.n1.right = self.n2
        self.assertIs(self.n2.parent, self.n1)


class BinaryTreeTestCase(unittest.TestCase):
    def setUp(self):
        """ Creates the tree from the problem statement. """
        root = Node(5)
        root.left = Node(3)
        root.right = Node(7)
        root.left.left = Node(2)
        root.left.right = Node(5)
        root.right.left = Node(1)
        root.right.right = Node(0)
        root.right.right.left = Node(2)
        root.right.right.right = Node(8)
        root.right.right.right.right = Node(5)

        self.tree = BinaryTree(root)

    def test__validate(self):
        node = Node(0)
        node.left = Node(0)
        self.assertRaises(ValueError, self.tree._validate, node.left)

    def test_sum(self):
        self.assertEqual(self.tree.sum(), 38)
        self.assertEqual(self.tree.sum(self.tree.root.left.left), 2)
        self.assertEqual(self.tree.sum(self.tree.root.right), 23)

    def test_mean(self):
        self.assertAlmostEqual(self.tree.mean(), 3.8)
        self.assertAlmostEqual(self.tree.mean(self.tree.root.left.left), 2)
        self.assertAlmostEqual(self.tree.mean(self.tree.root.right), 23 / 6)

    def test_median(self):
        self.assertAlmostEqual(self.tree.median(), 4)
        self.assertAlmostEqual(self.tree.median(self.tree.root.left.left), 2)
        self.assertAlmostEqual(self.tree.median(self.tree.root.right), 3.5)


if __name__ == "__main__":
    unittest.main()

