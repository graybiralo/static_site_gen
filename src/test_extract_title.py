import unittest
from extract_title import extract_title 

class TestExtractTitle(unittest.TestCase):

    def test_single_h1_header(self):
        markdown = "# Title\nSome other content."
        self.assertEqual(extract_title(markdown), "Title")

    def test_multiple_headers(self):
        markdown = "# First Title\n## Subheader\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_h1_header(self):
        markdown = "## Subheader\nSome content."
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in the markdown.")

    def test_h1_with_extra_spaces(self):
        markdown = "#   Title With Extra Spaces   \nSome content."
        self.assertEqual(extract_title(markdown), "Title With Extra Spaces")

    def test_h1_with_no_text(self):
        markdown = "# \nSome content."
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "H1 header found but no text provided.")

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in the markdown.")

if __name__ == '__main__':
    unittest.main()
