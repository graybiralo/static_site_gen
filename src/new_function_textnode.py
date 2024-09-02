import re
from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            split_parts = node.text.split(delimiter)
            if len(split_parts) % 2 == 0:
                raise ValueError(f"unmatched delimeter '{delimiter}' found in ther text.")
            for i, part in enumerate(split_parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, "text", node.url))
                else:
                    new_nodes.append(TextNode(part, text_type, node.url))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            text = node.text
            images = extract_markdown_images(text)
            if not images:
                new_nodes.append(node)
                continue
            
            for alt_text, img_url in images:
                sections = text.split(f"![{alt_text}]({img_url})", 1)
                if sections[0]:  
                    new_nodes.append(TextNode(sections[0], "text", node.url))
                
                new_nodes.append(TextNode(alt_text, "image", img_url))
                
                text = sections[1]  
            
            if text: 
                new_nodes.append(TextNode(text, "text", node.url))
        else:
            new_nodes.append(node)
    
    return new_nodes or old_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            text = node.text
            links = extract_markdown_links(text)
            if not links:
                new_nodes.append(node)
                continue
            
            for anchor_text, link_url in links:
                sections = text.split(f"[{anchor_text}]({link_url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], "text", node.url))
                
                new_nodes.append(TextNode(anchor_text, "link", link_url))
                
                text = sections[1] 
            
            if text:
                new_nodes.append(TextNode(text, "text", node.url))
        else:
            new_nodes.append(node)
    
    return new_nodes or old_nodes 


def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"

    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)


    return [node for node in nodes if node.text]


