from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    accept_delim = ["*", "**", "`"]

    if delimiter not in accept_delim:
        raise Exception("That's invalid Markdown syntax")

    
    output_nodes = []
    
    for node in old_nodes:
        if node.text_type != "text":
            output_nodes.append(node)
        else:
            if delimiter in node.text:
                text_without_delimiter = node.text.split(delimiter)
                counter = -1

                for text in text_without_delimiter:
                    if text.count("*") % 2 != 0 or text.count("**") % 2 != 0 or text.count("`") % 2 != 0:
                        raise Exception("Mismatched closing delimiter")
                    
                    counter += 1

                    if text == '':
                        continue

                    if counter % 2 == 0:
                        output_nodes.append(TextNode(text, "text"))
                    else:
                        output_nodes.append(TextNode(text, text_type))

            else:
                output_nodes.append(node)

    return output_nodes

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
    
    output_nodes = []
    
    for node in old_nodes:
        if re.findall(r"\]\s+\(", node.text):
            raise Exception("That's some bad markdown language")
        
        if node.text_type != "text":
            output_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            if node.text:
                output_nodes.append(node)
                continue
            else:
                return []

        text_without_image = node.text.split(f"![{images[0][0]}]({images[0][1]})")

        if text_without_image[0] == '':
            output_nodes.append(TextNode(images[0][0], "image", images[0][1]))
            output_nodes.extend(split_nodes_image([TextNode(text_without_image[1], "text")]))
        else:
            output_nodes.append(TextNode(text_without_image[0], "text"))
            output_nodes.append(TextNode(images[0][0], "image", images[0][1]))
            output_nodes.extend(split_nodes_image([TextNode(text_without_image[1], "text")]))
    
    return output_nodes

def split_nodes_link(old_nodes):
    if not old_nodes:
        raise Exception("Where the nodes at?")
    
    output_nodes = []
    
    for node in old_nodes:
        if re.findall(r"\]\s+\(", node.text):
            raise Exception("That's some bad markdown language")
        
        if node.text_type != "text":
            output_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            if node.text:
                output_nodes.append(node)
                continue
            else:
                return []

        text_without_link = node.text.split(f"[{links[0][0]}]({links[0][1]})")

        if text_without_link[0] == '':
            output_nodes.append(TextNode(links[0][0], "link", links[0][1]))
            output_nodes.extend(split_nodes_link([TextNode(text_without_link[1], "text")]))
        else:
            output_nodes.append(TextNode(text_without_link[0], "text"))
            output_nodes.append(TextNode(links[0][0], "link", links[0][1]))
            output_nodes.extend(split_nodes_link([TextNode(text_without_link[1], "text")]))
    
    return output_nodes

def text_to_textnodes(text):
    node = [TextNode(text, "text")]
    split_markdown = node
    split_markdown = split_nodes_delimiter(node, "**", "bold")
    split_markdown = split_nodes_delimiter(split_markdown, "*", "italic")
    split_markdown = split_nodes_delimiter(split_markdown, "`", "code")
    split_markdown = split_nodes_image(split_markdown)
    split_markdown = split_nodes_link(split_markdown)

    return split_markdown

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")

    clean_blocks = [x.strip() for x in split_blocks if x.strip()]

    return clean_blocks

def block_to_block_type(text):
    if re.search("^#{1,6}\s", text):
        return "heading"
    if text.startswith("```") and text.endswith("```"):
        return "code"
    if text.startswith(">"):
        quote_split = [x.strip() for x in text.split("\n")]
        if all(x[0] == ">" for x in quote_split):
            return "quote"
    if text.startswith("* ") or text.startswith("- "):
        unordered_split = [x.strip() for x in text.split("\n")]
        if all(x.startswith("* ") for x in unordered_split) or all(x.startswith("- ") for x in unordered_split):
            return "unordered"
    if text.startswith("1. "):
        ordered_split = [x.strip() for x in text.split("\n")]

        for i in range(0, len(ordered_split)):
            if ordered_split[i].startswith(f"{i + 1}. "):
                if i == (len(ordered_split) - 1):
                    return "ordered"
                continue
            else:
                break
    
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks_of_markdown = markdown_to_blocks(markdown)
    div_block = []
    for block in blocks_of_markdown:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                div_block.append(heading_to_html(block))
            case "code":
                div_block.append(code_to_html(block))
            case "quote":
                div_block.append(quote_to_html(block))
            case "unordered":
                div_block.append(unordered_to_html(block))
            case "ordered":
                div_block.append(ordered_to_html(block))
            case "paragraph":
                div_block.append(paragraph_to_html(block))
    return ParentNode(div_block, "div")
            
def heading_to_html(block):
    header_num = len(block.split()[0])
    return ParentNode(text_to_children(block[header_num + 1:]), f"h{header_num}")

def code_to_html(block):
    return ParentNode([ParentNode([LeafNode(block[3:-3], None)], "code")], "pre")

def quote_to_html(block):
    return ParentNode(text_to_children(block.replace("> ", "")), "blockquote")

def unordered_to_html(block):
    if block.startswith("* "):
        split_block = block.split("* ")[1:]
    else:
        split_block = block.split("- ")[1:]

    return ParentNode(list(map(lambda x: ParentNode(text_to_children(x.strip()), "li"), split_block)), "ul")

def ordered_to_html(block):
    ordered_split = [x.strip() for x in block.split("\n")]

    for i in range(0, len(ordered_split)):
        ordered_split[i] = ordered_split[i].replace(f"{i + 1}. ", "")

    return ParentNode(list(map(lambda x: ParentNode(text_to_children(x), "li"), ordered_split)), "ol")

def paragraph_to_html(block):
    return ParentNode(text_to_children(block), "p")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes