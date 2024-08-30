import unittest

from textnode import TextNode, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def text_neq_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def text_neq_different_style(self):
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
        
if __name__ == "__main__":
    unittest.main()