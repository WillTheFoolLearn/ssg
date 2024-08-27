from textnode import TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    accept_delim = ["*", "**", "`"]

    if delimiter not in accept_delim:
        raise Exception("That's invalid Markdown syntax")

    if not old_nodes:
        raise Exception("Where the nodes at?")
    
    split_node = []
    
    for node in old_nodes:
        if delimiter in node.text:
            node_split = node.text.split(delimiter)
            if node.text.startswith(delimiter):
                for i in range(1, len(node_split)):
                    add_to_split(text_type, split_node, node_split, i)
            else:
                for i in range(0, len(node_split)):
                    add_to_split(text_type, split_node, node_split, i)
        else:
            split_node.append(node)
    return split_node

def add_to_split(text_type, split_node, node_split, i):
    if i % 2 == 0:
        split_node.append(TextNode(node_split[i], "text"))
    else:
        split_node.append(TextNode(node_split[i], text_type))

def extract_markdown_images(text):
    all_alt_text = re.findall(r"!\[(.*?)\]", text)
    all_links = re.findall(r"\((.*?)\)", text)
    return list(zip(all_alt_text, all_links))

def extract_markdown_links(text):
    all_anchor_text = re.findall(r"\[(.*?)\]", text)
    all_urls = re.findall(r"\((.*?)\)", text)
    return list(zip(all_anchor_text, all_urls))

def split_nodes_image(old_nodes):
    if not old_nodes:
        raise Exception("Where the nodes at?")
    
    split_node = []
    
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        print(images)
        if images:
            for image in images:
                node_split = node.text.split(f"![{image[0]}]({image[1]})")
                if node_split[0]:
                    split_node.append(TextNode(node_split[0], "text"))
                    split_node.append(TextNode(node_split[1], image[0], image[1]))
                    split_node.append(TextNode(node_split[2], "text"))
                else:
                    split_node.append(TextNode(node_split[0], image[0], image[1]))
                    split_node.append(TextNode(node_split[1], "text"))
        else:
            raise Exception("No images to extract")
        
    return split_node