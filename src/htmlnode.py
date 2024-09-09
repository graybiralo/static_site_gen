class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("This method should be overridden in child classes.")
    
    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)
        if value is None:
            raise ValueError("The 'value' argument is required for LeafNode.")
    
    def to_html(self):
        if not self.value and self.tag not in ["input", "img"]:
            raise ValueError("LeafNode must have a non-empty value.")
        
        props_html = self.props_to_html()
        
        if self.tag in ["", None]:
            return self.value
        
        # Handle self-closing tags like <input>, <img>
        if self.tag in ["input", "img"]:
            return f"<{self.tag}{props_html}>"
        
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
 
def text_node_to_html_node(text_node):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url

    if text_type == "text":
        return LeafNode(tag=None, value=text)
    elif text_type == "bold":
        return LeafNode(tag="b", value=text)
    elif text_type == "italic":
        return LeafNode(tag="i", value=text)
    elif text_type == "code":
        return LeafNode(tag="code", value=text)
    elif text_type == "link":
        if not url:
            raise ValueError("Link TextNode must have a URL.")
        return LeafNode(tag="a", value=text, props={"href": url})
    elif text_type == "image":
        if not url:
            raise ValueError("Image TextNode must have a URL.")
        return LeafNode(tag="img", value="", props={"src": url, "alt": text})
    else:
        raise ValueError(f"Unsupported text_type: {text_type}")



class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None or not children:
            raise ValueError("ParentNode must have at least one child.")
        if not isinstance(children, list):
            raise TypeError("children must be a list.")
        if not all(isinstance(child, HTMLNode) for child in children):
            raise TypeError("All children must be instances of HTMLNode.")
        
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have at least one child.")
        
        children_html = ''.join(child.to_html() for child in self.children)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"




