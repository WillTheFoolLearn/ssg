import unittest

from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node with **bolded text inside** the node", "bold")
        node2 = TextNode("This is a text node with **bolded text inside** the node", "bold")
        new_node = split_nodes_delimiter([node], "**", "bold")
        new_node2 = split_nodes_delimiter([node2], "**", "bold")
        self.assertEqual(new_node, new_node2)

    def test_eq2(self):
        node = TextNode('This is a text node with **bolded text inside** the node and *italics tucked in* as well', "bold")
        new_node = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(new_node, [TextNode('This is a text node with ' , 'text'), TextNode('bolded text inside', 'bold'), TextNode( ' the node and *italics tucked in* as well', 'text')])
    
    def test_eq3(self):
        node = TextNode('This is a text node with **bolded text inside** the node and *italics tucked in* as well', "bold")
        new_node = split_nodes_delimiter(split_nodes_delimiter([node], "**", "bold"), "*", "italic")
        self.assertEqual(new_node, [TextNode('This is a text node with ' , 'text'), TextNode('bolded text inside', 'bold'), TextNode( ' the node and ', 'text'), TextNode( 'italics tucked in', 'italic'), TextNode( ' as well', 'text')])  

    def test_eq4(self):
        node = TextNode('`Code is the best` says the coded coder', "code")
        new_node = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(new_node, [TextNode('Code is the best', 'code'), TextNode(' says the coded coder', 'text')])

    def test_eq5(self):
        node = TextNode('`Code is the best` **boldly said** says the coded coder', "code")
        new_node = split_nodes_delimiter(split_nodes_delimiter([node], "`", "code"), "**", "bold")
        self.assertEqual(new_node, [TextNode('Code is the best', 'code'), TextNode(' ', 'text'), TextNode('boldly said', 'bold'), TextNode(' says the coded coder', 'text')])

    # def test_eq6(self):
    #     node = TextNode('*Inside this italics is a **bolded statement** but the whole thing* is not in italics', "**", "bold")
    #     new_node  = split_nodes_delimiter(split_nodes_delimiter([node], "**", "bold"), "*", "italic")
    #     self.assertEqual(new_node, [TextNode('Inside this italics is a ', 'italic'), TextNode("bolded statement", "bold"), TextNode(" but the whole thing", "italic"), TextNode(" is not in italics", "italic")])

    def test_eq7(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_eq8(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]) 

    def test_eq9(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "image")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("This is text with a ", "text_type_text"), TextNode("rick roll", "text_type_link", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text_type_text"), TextNode("obi wan", "text_type_link", "https://i.imgur.com/fJRm4Vk.jpeg"),])
    

if __name__ == "__main__":
    unittest.main()