import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
 
#testCases for HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(tag="img", props={"src": "image.jpg", "alt": "A beautiful scenery", "width": "600"})
        self.assertEqual(node.props_to_html(), ' src="image.jpg" alt="A beautiful scenery" width="600"')

    def test_repr(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "https://www.google.com"})
        expected_repr = "HTMLNode(tag='a', value='Google', children=[], props={'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_children(self):
        child_node = HTMLNode(tag="span", value="Click here")
        node = HTMLNode(tag="a", children=[child_node], props={"href": "https://www.example.com"})
        expected_repr = (
            "HTMLNode(tag='a', value=None, children=[HTMLNode(tag='span', value='Click here', "
            "children=[], props={})], props={'href': 'https://www.example.com'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_no_tag_value_or_props(self):
        node = HTMLNode()
        expected_repr = "HTMLNode(tag=None, value=None, children=[], props={})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html_with_special_characters(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://example.com?a=1&b=2"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com?a=1&b=2"')

#testCases for LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag(self):
        node = LeafNode(value="Hello, World!", tag="p", props={"class": "greeting"})
        expected_html = '<p class="greeting">Hello, World!</p>'
        self.assertEqual(node.to_html(), expected_html)
    
    def test_to_html_without_tag(self):
        node = LeafNode(value="Just text")
        expected_html = 'Just text'
        self.assertEqual(node.to_html(), expected_html)
    
    def test_to_html_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode(value="").to_html()
    
    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(value=None).to_html()

    def test_to_html_no_tag_with_non_empty_value(self):
        node = LeafNode(value="Some text")
        expected_html = 'Some text'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_special_characters(self):
        node = LeafNode(value="Hello & Welcome!", tag="p")
        expected_html = '<p>Hello & Welcome!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_boolean_props(self):
        node = LeafNode(value="Check me", tag="input", props={"type": "checkbox", "checked": ""})
        expected_html = '<input type="checkbox" checked="">'
        self.assertEqual(node.to_html(), expected_html)

#testCases for ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_tag_and_children(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        expected_html = '<div><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)


    def test_to_html_with_nested_parent_nodes(self):
        child1 = LeafNode(value="Child 1", tag="span")
        child2 = LeafNode(value="Child 2", tag="span")
        nested_parent = ParentNode(tag="section", children=[child1])
        parent = ParentNode(tag="div", children=[nested_parent, child2])
        expected_html = '<div><section><span>Child 1</span></section><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)
    
    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=[]).to_html()

    def test_to_html_without_tag(self):
        child1 = LeafNode(value="Child 1", tag="span")
        with self.assertRaises(ValueError):
            ParentNode(children=[child1]).to_html()

    def test_to_html_with_multiple_children_and_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected_html = '<div class="container"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)


    def test_to_html_with_invalid_children_type(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="div", children="Invalid Child Type")

    def test_repr_with_nested_parent_nodes(self):
        child = LeafNode(tag="span", value="Child 1")
        section = ParentNode(tag="section", children=[child])
        parent = ParentNode(tag="div", children=[section])
        expected_repr = (
            "HTMLNode(tag='div', value=None, children=[HTMLNode(tag='section', value=None, "
            "children=[HTMLNode(tag='span', value='Child 1', children=[], props={})], props={})], props={})"
        )
        self.assertEqual(repr(parent), expected_repr)

    def test_to_html_with_mixed_children(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = ParentNode(tag="section", children=[LeafNode(tag="p", value="Nested Child")])
        parent = ParentNode(tag="div", children=[child1, child2])
        expected_html = '<div><span>Child 1</span><section><p>Nested Child</p></section></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_multiple_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        parent = ParentNode(tag="div", children=[child1], props={"class": "container", "id": "parentDiv"})
        expected_html = '<div class="container" id="parentDiv"><span>Child 1</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_deeply_nested_nodes(self):
        nested_child = LeafNode(tag="b", value="Bold Text")
        section = ParentNode(tag="section", children=[nested_child])
        parent = ParentNode(tag="div", children=[section])
        wrapper = ParentNode(tag="div", children=[parent], props={"class": "wrapper"})
        expected_html = '<div class="wrapper"><div><section><b>Bold Text</b></section></div></div>'
        self.assertEqual(wrapper.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()