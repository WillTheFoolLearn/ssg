import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("Cheddar is the best cheese", "italic", "www.cheese.com")
        node2 = TextNode("Cheddar is the worst cheese", "italic", "www.cheese.com")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("Please make a new SSX", "bold", None)
        node2 = TextNode("Please make a new SSX", "bold")
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("Tiny riots are still riots", "bold")
        node2 = TextNode("Tiny riots are still riots", "italic")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()