import unittest

from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_image,
        text_type_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq1(self):
        node = TextNode("123", text_type_italic, "www.fuckyou.com")
        node2 = TextNode("123", text_type_italic, "www.fuckyou.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("123", text_type_code)
        node2 = TextNode("123", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_neq1(self):
        node = TextNode("123", text_type_code, "www.fuckme.com")
        node2 = TextNode("123", text_type_code)
        self.assertNotEqual(node, node2)

if __name__=="__main__":
    unittest.main()
