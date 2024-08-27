import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def text_neq_different_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertEqual(node, node2)

    def text_neq_different_style(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertEqual(node, node2)

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
        
if __name__ == "__main__":
    unittest.main()