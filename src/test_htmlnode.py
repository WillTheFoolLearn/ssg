import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "I am hungry", [], {"align": "center"})
        node2 = HTMLNode("p", "I am hungry", [], {"align": "center"})
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("a", "I am hungry", [], {"href": "www.cheese.com"})
        node2 = HTMLNode("p", "I am hungry", [], {"href": "www.cheese.com"})
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode("h1", "", ["body"])
        node2 = HTMLNode("h1", "", ["body"])
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = HTMLNode("p", "I am dad", [], {"align": "center"})
        node2 = HTMLNode("p", "I am dad", ["h1"], {"align": "center"})
        self.assertNotEqual(node, node2)

    def test_eq5(self):
        node = LeafNode("I am dad", "p", {"align": "center"})
        node2 = LeafNode("I am dad", "p", {"align": "center"})
        self.assertEqual(node, node2)

    def test_eq6(self):
        node = LeafNode("I am dad", "a", {"align": "center"})
        node2 = LeafNode("I am dad", "p", {"align": "center"})
        self.assertNotEqual(node, node2)
    
    def test_eq7(self):
        node = LeafNode("p", "I am dad")
        node2 = LeafNode("p", "I am dad", {"align": "center"})
        self.assertNotEqual(node, node2)

    def test_eq8(self):
        node = LeafNode("p", "I am dad", {"align": "center"})
        node2 = LeafNode("I am dad", {"align": "center"})
        self.assertNotEqual(node, node2)

    def test_eq9(self):
        node = LeafNode("p", "I am dad", {"align": "center"})
        node2 = LeafNode("p", "I am dad", {"align": "left"})
        self.assertNotEqual(node, node2)

    def test_eq10(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        self.assertEqual(node, node2)

    def test_eq11(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"), 
                ParentNode([
                    LeafNode("a", "Yahoo text", {"href": "www.yahoo.com"}),
                    LeafNode("a", "Google text", {"href": "www.google.com"}),
                ], "b"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode([
                    LeafNode("a", "Yahoo text", {"href": "www.yahoo.com"}),
                    LeafNode("a", "Google text", {"href": "www.google.com"}),
                ], "b"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        self.assertEqual(node, node2)

    def test_eq12(self):
        node = ParentNode(
            [],"p", {"align": "center"})
        node2 = ParentNode(
            [],"p", {"align": "center"})
        self.assertEqual(node, node2)
    
    def test_eq13(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
            ],"p", {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        self.assertNotEqual(node, node2)

    def test_eq14(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ], {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ], {"align": "center"})
        self.assertEqual(node, node2)

    def test_eq15(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p")
        node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p")
        self.assertEqual(node, node2)

    def test_eq16(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ], {"align": "center"}, "p")
        node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],"p", {"align": "center"})
        self.assertNotEqual(node, node2)

    def test_eq17(self):
        node = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ], "p", {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ], "p", {"align": "center"})
        self.assertEqual(node.to_html(), node2.to_html())

    def test_eq18(self):
        node = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None), 
                ParentNode([
                    LeafNode("Yahoo text", "a", {"href": "www.yahoo.com"}),
                    LeafNode("Google text", "a",  {"href": "www.google.com"}),
                ], "b"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],"p", {"align": "center"})
        node2 = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None), 
                ParentNode([
                    LeafNode("Yahoo text", "a", {"href": "www.yahoo.com"}),
                    LeafNode("Google text", "a",  {"href": "www.google.com"}),
                ], "b"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],"p", {"align": "center"})
        self.assertEqual(node.to_html(), node2.to_html())

    def test_eq19(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(text_node_to_html_node(node), text_node_to_html_node(node2))
    
    def test_eq20(self):
        node = TextNode("This is a text node", "link", "www.webcrawler.com")
        node2 = TextNode("This is a text node", "link", "www.webcrawler.com")
        self.assertEqual(text_node_to_html_node(node), text_node_to_html_node(node2))


if __name__ == "__main__":
    unittest.main()