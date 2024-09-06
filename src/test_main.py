import unittest
from main import extract_title

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        markdown = "# Simple header test"
        self.assertEqual(extract_title(markdown), "Simple header test")

    def test_eq2(self):
        markdown = "## This shouldn't work"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_eq3(self):
        markdown = "#555-434-3323"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_eq4(self):
        markdown = "     # Header with space!"
        self.assertEqual(extract_title(markdown), "Header with space!")

if __name__ == "__main__":
    unittest.main()