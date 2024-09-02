import unittest

from textnode import TextNode
from new_function_textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

#Testcase for TextNode

class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_different_style(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_link(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_neq_different_link(self):
        node = TextNode("This is a text node", "bold", "https://www.same.com")
        node2 = TextNode("This is a text node", "bold", "https://www.different.com")
        self.assertNotEqual(node, node2)

    def test_eq_full_properties(self):
        node = TextNode("This is a text node", "bold", "https://www.same.com")
        node2 = TextNode("This is a text node", "bold", "https://www.same.com")
        self.assertEqual(node, node2)


#Testcase for SplitNodesDelimeter

class TestSplitNodesDelimeter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(result, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("This is **bolded** text", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(result, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("This is *italicized* text", "text")
        result = split_nodes_delimiter([node], "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("italicized", "italic"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(result, expected)


#Testcase for MarkdownExtraction

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is an image ![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        text = "![img1](https://example.com/img1.jpg) and ![img2](https://example.com/img2.jpg)"
        result = extract_markdown_images(text)
        expected = [
            ("img1", "https://example.com/img1.jpg"),
            ("img2", "https://example.com/img2.jpg"),
        ]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_edge_case(self):
        text = "![alt text]()"
        result = extract_markdown_images(text)
        expected = [("alt text", "")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_single(self):
        text = "This is a link [click here](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("click here", "https://example.com")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links_multiple(self):
        text = "[link1](https://example.com/1) and [link2](https://example.com/2)"
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links_ignores_images(self):
        text = "![image](https://example.com/img.jpg) and [link](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_edge_case(self):
        text = "[empty link]()"
        result = extract_markdown_links(text)
        expected = [("empty link", "")]
        self.assertEqual(result, expected)


#Testcase for split_nodes_images_andd_links

class TestsplitNodes(unittest.TestCase):
    def test_split_nodes_image_single(self):
        node = TextNode("Here is an image ![example](https://example.com/image.png)", "text")
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an image ", "text"),
            TextNode("example", "image", "https://example.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("First ![one](https://example.com/one.png) and second ![two](https://example.com/two.png)", "text")
        result = split_nodes_image([node])
        expected = [
            TextNode("First ", "text"),
            TextNode("one", "image", "https://example.com/one.png"),
            TextNode(" and second ", "text"),
            TextNode("two", "image", "https://example.com/two.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_image(self):
        node = TextNode("There is no image here.", "text")
        result = split_nodes_image([node])
        expected = [node]
        self.assertEqual(result, expected)

    def test_split_nodes_image_empty_text(self):
        node = TextNode("", "text")
        result = split_nodes_image([node])
        expected = [node]
        self.assertEqual(result, expected)
    
    def test_split_nodes_image_malformed_markdown(self):
        node = TextNode("Here is ![malformed image(https://example.com/image.png)", "text")
        result = split_nodes_image([node])
        expected = [node]
        self.assertEqual(result, expected)
    
    def test_split_nodes_link_single(self):
        node = TextNode("Visit [Google](https://www.google.com)", "text")
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", "text"),
            TextNode("Google", "link", "https://www.google.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("[GitHub](https://github.com) and [StackOverflow](https://stackoverflow.com)", "text")
        result = split_nodes_link([node])
        expected = [
            TextNode("GitHub", "link", "https://github.com"),
            TextNode(" and ", "text"),
            TextNode("StackOverflow", "link", "https://stackoverflow.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_link(self):
        node = TextNode("This text has no links.", "text")
        result = split_nodes_link([node])
        expected = [node]
        self.assertEqual(result, expected)

    def test_split_nodes_link_empty_text(self):
        node = TextNode("", "text")
        result = split_nodes_link([node])
        expected = [node]
        self.assertEqual(result, expected)

    def test_split_nodes_link_malformed_markdown(self):
        node = TextNode("Here is a [broken link(https://example.com)", "text")
        result = split_nodes_link([node])
        expected = [node]
        self.assertEqual(result, expected)

#testcase for text to textnode

class TestTextNodeFunctions(unittest.TestCase):
    def test_basic_text(self):
        text = "Hello world"
        expected_nodes = [
            TextNode("Hello world", "text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_bold_text(self):
        text = "This is **bold** text"
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_italic_text(self):
        text = "This is *italic* text"
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_code_text(self):
        text = "This is `code` text"
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" text", "text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_image(self):
        text = "This is an ![image](https://example.com/image.png)"
        expected_nodes = [
            TextNode("This is an ", "text"),
            TextNode("image", "image", "https://example.com/image.png")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_link(self):
        text = "This is a [link](https://example.com)"
        expected_nodes = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_combined(self):
        text = "Here is **bold** text, *italic*, `code`, an ![image](https://example.com/image.png), and a [link](https://example.com)."
        expected_nodes = [
            TextNode("Here is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text, ", "text"),
            TextNode("italic", "italic"),
            TextNode(", ", "text"),
            TextNode("code", "code"),
            TextNode(", an ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
            TextNode(", and a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(".", "text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_unmatched_delimiter(self):
        text = "This is **bold text without closing delimiter"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_empty_text(self):
        text = ""
        expected_nodes = []
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)

    def test_text_with_only_formatting(self):
        text = "**bold** *italic* `code`"
        expected_nodes = [
            TextNode("bold", "bold"),
            TextNode(" ", "text"),
            TextNode("italic", "italic"),
            TextNode(" ", "text"),
            TextNode("code", "code")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)


if __name__ == "__main__":
    unittest.main()