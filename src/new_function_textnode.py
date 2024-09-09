import re
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

# Split nodes on delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            split_parts = node.text.split(delimiter)
            if len(split_parts) % 2 == 0:
                raise ValueError(f"Unmatched delimiter '{delimiter}' found in the text.")
            for i, part in enumerate(split_parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, "text", node.url))
                else:
                    new_nodes.append(TextNode(part, text_type, node.url))
        else:
            new_nodes.append(node)
    return new_nodes

# Extract markdown images and links using regex
def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_pattern, text)
    return matches

# Split nodes on images
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

# Split nodes on links
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

# Converting text to textnode
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

    # Remove leading and trailing whitespace/newlines from code blocks
    for node in nodes:
        if isinstance(node, TextNode) and node.text_type == "code":
            node.text = node.text.strip()

    return [node for node in nodes if node.text]

# Function for markdown to blocks
def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split('\n\n') if block.strip()]
    cleaned_blocks = []
    for block in blocks:
        cleaned_block = '\n'.join(line.strip() for line in block.splitlines())
        cleaned_blocks.append(cleaned_block)
    return cleaned_blocks

# Function for block to block type
def block_to_block_type(block):
    block = block.strip()
    if not block:
        return 'paragraph'
    if block.startswith("```") and block.endswith("```"):
        return 'code'
    if block.startswith('#'):
        if ' ' in block[1:]:
            return 'heading'
    if all(line.startswith('>') for line in block.splitlines()):
        return 'quote'
    if all(line.startswith(('* ', '- ')) for line in block.splitlines()):
        return 'unordered_list'
    
    ordered_list_pattern = re.compile(r'^\d+\.\s')
    if all(ordered_list_pattern.match(line.lstrip()) for line in block.splitlines()):
        return 'ordered_list'
    
    return 'paragraph'

# Function to convert text to HTML nodes
def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

# Convert a markdown document to an HTMLNode
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == 'paragraph':
            html_nodes.append(ParentNode(tag="p", children=text_to_children(block.strip())))
        elif block_type == 'code':
            code_content = block.strip("```").strip()
            html_nodes.append(ParentNode(tag="pre", children=[
                ParentNode(tag="code", children=[LeafNode(tag=None, value=code_content)])
            ]))
        elif block_type == 'heading':
            # Count the heading level and clean the heading text
            level = block.count('#')
            heading_content = block.strip('#').strip()
            html_nodes.append(ParentNode(tag=f"h{level}", children=[LeafNode(tag=None, value=heading_content)]))
        elif block_type == 'quote':
            quote_content = block.strip('> ').strip()
            html_nodes.append(ParentNode(tag="blockquote", children=[LeafNode(tag=None, value=quote_content)]))
        elif block_type == 'unordered_list':
            items = [ParentNode(tag="li", children=[LeafNode(tag=None, value=item.strip('* - ').strip())])
                     for item in block.splitlines()]
            html_nodes.append(ParentNode(tag="ul", children=items))
        elif block_type == 'ordered_list':
            ordered_list_pattern = re.compile(r'^\d+\.\s*')
            items = [ParentNode(tag="li", children=[LeafNode(tag=None, value=ordered_list_pattern.sub("", item).strip())])
                     for item in block.splitlines()]
            html_nodes.append(ParentNode(tag="ol", children=items))
        else:
            html_nodes.append(ParentNode(tag="p", children=text_to_children(block.strip())))

    return ParentNode(tag="div", children=html_nodes)


