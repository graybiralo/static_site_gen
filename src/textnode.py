class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
        return False
    
    def __repr__(self):
        return f"TextNode(text='{self.text!r}', text_type='{self.text_type!r}', url='{self.url!r}')"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            split_parts = node.text.split(delimiter)
            if len(split_parts) % 2 == 0:
                raise ValueError(f"unmatced delimeter '{delimiter}' found in ther text.")
            for i, part in enumerate(split_parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, "text", node.url))
                else:
                    new_nodes.append(TextNode(part, text_type, node.url))
        else:
            new_nodes.append(node)
    return new_nodes