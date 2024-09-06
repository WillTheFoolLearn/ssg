import unittest

from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, heading_to_html, markdown_to_html_node
from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node with **bolded text inside** the node", "text")
        node2 = TextNode("This is a text node with **bolded text inside** the node", "text")
        new_node = split_nodes_delimiter([node], "**", "bold")
        new_node2 = split_nodes_delimiter([node2], "**", "bold")
        self.assertEqual(new_node, new_node2)

    def test_eq2(self):
        node = TextNode('This is a text node with **bolded text inside** the node and *italics tucked in* as well', "text")
        new_node = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(new_node, [TextNode('This is a text node with ' , 'text'), TextNode('bolded text inside', 'bold'), TextNode( ' the node and *italics tucked in* as well', 'text')])
    
    def test_eq3(self):
        node = TextNode('This is a text node with **bolded text inside** the node and *italics tucked in* as well', "text")
        new_node = split_nodes_delimiter(split_nodes_delimiter([node], "**", "bold"), "*", "italic")
        self.assertEqual(new_node, [TextNode('This is a text node with ' , 'text'), TextNode('bolded text inside', 'bold'), TextNode( ' the node and ', 'text'), TextNode( 'italics tucked in', 'italic'), TextNode( ' as well', 'text')])  

    def test_eq4(self):
        node = TextNode('`Code is the best` says the coded coder', "text")
        new_node = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(new_node, [TextNode('Code is the best', 'code'), TextNode(' says the coded coder', 'text')])

    def test_eq5(self):
        node = TextNode('`Code is the best` **boldly said** says the coded coder', "text")
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
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("This is text with a ", "text"), TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text"), TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),])
    
    def test_eq10(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and some additional text", "text")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("This is text with a ", "text"), TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text"), TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and some additional text", "text")])
    
    def test_eq11(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) but there's no space in between the images!", "text")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("This is text with a ", "text"), TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" but there's no space in between the images!", "text")])

    def test_eq12(self):
        node = TextNode("This is text with a ![rick roll] (https://i.imgur.com/aKaOqIh.gif) and ![obi wan] (https://i.imgur.com/fJRm4Vk.jpeg) and some additional text", "text")
        with self.assertRaises(Exception):
            split_nodes_image([node])

    def test_eq13(self):
        node = TextNode("This is text with a ![ rick roll ](https://i.imgur.com/aKaOqIh.gif) and ![obi    wan     ](  https://i.imgur.com/fJRm4Vk.jpeg   ) and some additional text", "text")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("This is text with a ", "text"), TextNode(" rick roll ", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text"), TextNode("obi    wan     ", "image", "  https://i.imgur.com/fJRm4Vk.jpeg   "), TextNode(" and some additional text", "text")])

    def test_eq14(self):
        node = TextNode("This is text with a [WaniKani](https://www.wanikani.com/) and [The Fool's Twitch](https://www.twitch.tv/willthefoollearn)", "text")
        split_link = split_nodes_link([node])
        self.assertEqual(split_link, [TextNode("This is text with a ", "text"), TextNode("WaniKani", "link", "https://www.wanikani.com/"), TextNode(" and ", "text"), TextNode("The Fool's Twitch", "link", "https://www.twitch.tv/willthefoollearn"),])
    
    def test_eq15(self):
        node = TextNode("This is text with a [WaniKani](https://www.wanikani.com/) and [The Fool's Twitch](https://www.twitch.tv/willthefoollearn) and some additional text", "text")
        split_link = split_nodes_link([node])
        self.assertEqual(split_link, [TextNode("This is text with a ", "text"), TextNode("WaniKani", "link", "https://www.wanikani.com/"), TextNode(" and ", "text"), TextNode("The Fool's Twitch", "link", "https://www.twitch.tv/willthefoollearn"), TextNode(" and some additional text", "text")])
    
    def test_eq15(self):
        node = TextNode("This is text with a [WaniKani](https://www.wanikani.com/)[The Fool's Twitch](https://www.twitch.tv/willthefoollearn) and some additional text", "text")
        split_link = split_nodes_link([node])
        self.assertEqual(split_link, [TextNode("This is text with a ", "text"), TextNode("WaniKani", "link", "https://www.wanikani.com/"), TextNode("The Fool's Twitch", "link", "https://www.twitch.tv/willthefoollearn"), TextNode(" and some additional text", "text")])

    def test_eq16(self):
        node = TextNode("This is text with a [WaniKani]  (https://www.wanikani.com/) and [The Fool's Twitch]  (https://www.twitch.tv/willthefoollearn) and some additional text", "text")
        with self.assertRaises(Exception):
            split_nodes_link([node])

    def test_eq17(self):
        node = TextNode("This is text with a [  WaniKani   ](   https://www.wanikani.com/) and [The Fool's Twitch   ](       https://www.twitch.tv/willthefoollearn)", "text")
        split_link = split_nodes_link([node])
        self.assertEqual(split_link, [TextNode("This is text with a ", "text"), TextNode("  WaniKani   ", "link", "   https://www.wanikani.com/"), TextNode(" and ", "text"), TextNode("The Fool's Twitch   ", "link", "       https://www.twitch.tv/willthefoollearn"),])
    
    def test_eq18(self):
        node = TextNode("There are no images, oh no!", "text")
        split_images = split_nodes_image([node])
        self.assertEqual(split_images, [TextNode("There are no images, oh no!", "text")])

    def test_eq19(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split_text = text_to_textnodes(text)
        self.assertEqual(split_text, [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
            ])
    
    def test_eq20(self):
        node = TextNode("This ** oopsie * daisy ** what is * happening", "text")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node])

    def test_eq21(self):
        text = "This is *italic text* with a **bold** word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and a [link](https://boot.dev)"
        split_text = text_to_textnodes(text)
        self.assertEqual(split_text, [
            TextNode("This is ", "text"),
            TextNode("italic text", "italic"),
            TextNode(" with a ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
            ])
        
    def test_eq22(self):
        text = "This is *italic text* with a [link](https://boot.dev) and a **bold** word and more *italic text* and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and another [link](https://boot.dev)"
        split_text = text_to_textnodes(text)
        self.assertEqual(split_text, [
            TextNode("This is ", "text"),
            TextNode("italic text", "italic"),
            TextNode(" with a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
            TextNode(" and a ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word and more ", "text"),
            TextNode("italic text", "italic"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and another ", "text"),
            TextNode("link", "link", "https://boot.dev"),
            ])
        
    def test_eq23(self):
        text = "This is **text* with an **italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_eq24(self):
        text = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        cleaned = markdown_to_blocks(text)
        self.assertEqual(cleaned, [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item"""])
    
    def test_eq25(self):
        text = """
            # This is a heading







            This is a paragraph of text. It has some **bold** and *italic* words inside of it.



            

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        cleaned = markdown_to_blocks(text)
        self.assertEqual(cleaned, [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item"""])
        
    def test_eq26(self):
        text = """
            # This is a heading

                               This is a paragraph of text. It has some **bold** and *italic* words inside of it.                   

            * This is the first list item in a list block

            
                            * This is a list item
            * This is another list item"""
        cleaned = markdown_to_blocks(text)
        self.assertEqual(cleaned, [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
            "* This is the first list item in a list block",
            """* This is a list item
            * This is another list item"""])
        
    def test_eq27(self):
        text = "# This is a heading, right?"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_eq28(self):
        text = "```Got some code for you!```"
        self.assertEqual(block_to_block_type(text), "code")

    def test_eq29(self):
        text = """> I drink your milkshake
        > I drink it up!
        > It was delicious."""
        self.assertEqual(block_to_block_type(text), "quote")

    def test_eq30(self):
        text = """* Final Fantasy VI
        * Final Fantasy XII
        * Final Fantasy X"""
        self.assertEqual(block_to_block_type(text), "unordered")

    def test_eq31(self):
        text = """1. Jessie Rasberry
        2. Aerith Gainsborough
        3. Everyone else
        4. Tifa Shitbird"""
        self.assertEqual(block_to_block_type(text), "ordered")

    def test_eq32(self):
        text = "Oh, nothing else? Then it's a paragraph"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq33(self):
        text = "#This is an incorrect heading"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq34(self):
        text = "##### This is a heading, right?"
        self.assertEqual(block_to_block_type(text), "heading")
    
    def test_eq35(self):
        text = "####### Too many pounds so it's a paragraph"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq36(self):
        text = """* Final Fantasy VI
        * Final Fantasy XII
        - Final Fantasy X"""
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq37(self):
        text = """1. Jessie Rasberry
        2. Aerith Gainsborough
        3. Everyone else
        3. Tifa Shitbird"""
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq38(self):
        text = "``Got some code for you!``"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_eq39(self):
        test_header = heading_to_html("# Test header")
        self.assertEqual(test_header, ParentNode([LeafNode("Test header", None)], "h1"))

    def test_eq40(self):
        test_header = heading_to_html("### Test header")
        self.assertEqual(test_header, ParentNode([LeafNode("Test header", None)], "h3"))

    def test_eq41(self):
        test_markdown = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.                   

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        
        node = ParentNode([
            ParentNode([
                LeafNode("This is a heading", None),
            ], "h1"),
            ParentNode([
                LeafNode("This is a paragraph of text. It has some ", None),
                LeafNode("bold", "b"),
                LeafNode(" and ", None),
                LeafNode("italic", "i"),
                LeafNode(" words inside of it.", None)
            ], "p"),
            ParentNode([
                ParentNode([
                    LeafNode("This is the first list item in a list block", None)
                ], "li"),
                ParentNode([
                    LeafNode("This is a list item", None)
                ], "li"),
                ParentNode([
                    LeafNode("This is another list item", None)
                ], "li")
            ], "ul")
        ], "div")
        self.assertEqual(markdown_to_html_node(test_markdown), node)

    def test_eq42(self):
        test_markdown = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        
        node = ParentNode([
            ParentNode([
                LeafNode("This is a paragraph of text. It has some ", None),
                LeafNode("bold", "b"),
                LeafNode(" and ", None),
                LeafNode("italic", "i"),
                LeafNode(" words inside of it.", None)
            ], "p")
        ], "div")
        self.assertEqual(markdown_to_html_node(test_markdown), node)

    def test_eq43(self):
        test_markdown = """##### This is a heading

            ```This is a block of code. It has **bolded text** inside the code```

            1. This is the first list item in a list block
            2. This is a list item
            3. This is another list item"""
        
        node = ParentNode([
            ParentNode([
                LeafNode("This is a heading", None),
            ], "h5"),
            ParentNode([
                ParentNode([
                    LeafNode("This is a block of code. It has **bolded text** inside the code", None)
                ], "code")
            ], "pre"),
            ParentNode([
                ParentNode([
                    LeafNode("This is the first list item in a list block", None)
                ], "li"),
                ParentNode([
                    LeafNode("This is a list item", None)
                ], "li"),
                ParentNode([
                    LeafNode("This is another list item", None)
                ], "li")
            ], "ol")
        ], "div")
        self.assertEqual(markdown_to_html_node(test_markdown), node)

    def test_eq44(self):
        test_markdown = """##### This is a heading
            ```This is a block of code. It has **bolded text** inside the code```"""
        with self.assertRaises(Exception):
            markdown_to_html_node(test_markdown)
        

if __name__ == "__main__":
    unittest.main()