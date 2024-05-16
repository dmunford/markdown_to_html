import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_image,
        text_type_link,
    )
from html_include import (
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes,
    )
from block import (
        block_type_paragraph,
        block_type_heading,
        block_type_code,
        block_type_quote,
        block_type_unordered_list,
        block_type_ordered_list,
        markdown_to_blocks,
        block_to_block_type,
    )
from markdown import (
        markdown_to_html_node,
    )


class test_html_node(unittest.TestCase):
    def test1(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(props = props)
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")

class test_leaf_node(unittest.TestCase):
    def test1(self):
        props = {"href": "https://www.google.com"}
        node = LeafNode(tag="a", value="Click Me!", props=props)
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click Me!</a>")

class test_parent_node(unittest.TestCase):
    def test1(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold Text"),
                    LeafNode(None, "Normal Text"),
                    LeafNode("i", "Italic Text"),
                    LeafNode(None, "Normal Text"),
                ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold Text</b>Normal Text<i>Italic Text</i>Normal Text</p>")
    def test2(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold Text"),
                    LeafNode(None, "Normal Text"),
                    ParentNode(
                        "p",
                        [
                            LeafNode("i", "Italic Text"),
                            LeafNode(None, "NormalText"),
                        ],
                    ),
                    LeafNode("b", "Bold Text"),
                ],
            )
        r_text = "<p><b>Bold Text</b>Normal Text<p><i>Italic Text</i>NormalText</p><b>Bold Text</b></p>"
        self.assertEqual(node.to_html(), r_text)


class convert_node(unittest.TestCase):
    def test1(self):
        node = TextNode("Hello", text_type_text)
        r_test = "Hello"
        self.assertEqual(text_node_to_html_node(node).to_html(), r_test)

    def test2(self):
        node = TextNode("World", text_type_bold)
        r_test = "<b>World</b>"
        self.assertEqual(text_node_to_html_node(node).to_html(), r_test)

    def test3(self):
        node = TextNode("Click Me!", text_type_link, "www.google.com")
        r_test = "<a href=\"www.google.com\">Click Me!</a>"
        self.assertEqual(text_node_to_html_node(node).to_html(), r_test)

class split_node(unittest.TestCase):
    def test1(self):
        nodes = [
                TextNode("*Hello* World", text_type_text),
                TextNode("Hello `World`", text_type_text),
                TextNode("*Hell*o *World*", text_type_text),
        ]
        r_nodes = [
                TextNode("Hello", text_type_bold),
                TextNode(" World", text_type_text),
                TextNode("Hello `World`", text_type_text),
                TextNode("Hell", text_type_bold),
                TextNode("o ", text_type_text),
                TextNode("World", text_type_bold),
            ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", text_type_bold), r_nodes)

    def test_split_image(self):
        nodes = [
                TextNode("Text with ![image](imagelink) and ![image2](image2link)", text_type_text),
                TextNode("Text with no images", text_type_text),
                TextNode("![image3](imagelink3)", text_type_text),
                ]
        r_nodes = [
                TextNode("Text with ", text_type_text),
                TextNode("image", text_type_image, "imagelink"),
                TextNode(" and ", text_type_text),
                TextNode("image2", text_type_image, "image2link"),
                TextNode("Text with no images", text_type_text),
                TextNode("image3", text_type_image, "imagelink3"),
                ]
        self.assertEqual(split_nodes_image(nodes), r_nodes)

    def test_split_link(self):
        nodes = [
                TextNode("Text with [link](link) and [link2](link2)", text_type_text),
                TextNode("Text with no link", text_type_text),
                TextNode("[link3](link3)", text_type_text),
                ]
        r_nodes = [
                TextNode("Text with ", text_type_text),
                TextNode("link", text_type_link, "link"),
                TextNode(" and ", text_type_text),
                TextNode("link2", text_type_link, "link2"),
                TextNode("Text with no link", text_type_text),
                TextNode("link3", text_type_link, "link3"),
                ]
        self.assertEqual(split_nodes_link(nodes), r_nodes)

class extract_markdown(unittest.TestCase):
    def test1(self):
        text = "This is my shit. ![image_name](image1) and ![image_name2](image2) are images"
        r_test = [
                ("image_name", "image1"),
                ("image_name2", "image2"),
            ]
        self.assertEqual(extract_markdown_images(text), r_test)

    def test2(self):
        text = "This is my other shit. [link_name](link1) and [link_name2](link2) are links!"
        r_test = [
                ("link_name", "link1"),
                ("link_name2", "link2"),
            ]
        self.assertEqual(extract_markdown_links(text), r_test)

class text_to_node(unittest.TestCase):
    def test_to_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        r_test = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), r_test)

class blocks(unittest.TestCase):
    def test_blocks(self):
        markdown_text = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        r_out = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        blocks = markdown_to_blocks(markdown_text)
        self.assertEqual(blocks,r_out)

    def test_block2(self):
        markdown_text = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is a list item
        * This is another list item
        """
        r_out = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
                ]
        blocks = markdown_to_blocks(markdown_text)
        self.assertEqual(blocks, r_out)

    def test_block3(self):
        markdown_text = """
        # This is a heading


        This is a paragraph of text. It has some **bold** and *italic* words inside of it.


        * This is a list item
        * This is another list item
        """
        r_out = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
                ]
        blocks = markdown_to_blocks(markdown_text)
        self.assertEqual(blocks, r_out)

    def test_paragraph(self):
        markdown_text = """
            This is a standard paragraph, yay.
            """
        r_out = block_type_paragraph
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_heading(self):
        markdown_text = """
            # This is a heading
            """
        r_out = block_type_heading
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_heading1(self):
        markdown_text = """
            ### This is a heading
            """
        r_out = block_type_heading
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_code(self):
        markdown_text = """
            ``` This is code! ```
            """
        r_out = block_type_code
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_wrong_type(self):
        markdown_text = """
            ``` This is not code!.
            """
        r_out = block_type_paragraph
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_quote(self):
        markdown_text = """
            > This is a quote
            > This is also a quote
            > One more quote for good measure
            """
        r_out = block_type_quote
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_wrong_quote(self):
        markdown_text = """
            > This is a quote
            But this is not
            """
        r_out = block_type_paragraph
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_ulist(self):
        markdown_text = """
            * This is a ulist
            - This is a ulist
            * Also ulist
            """
        r_out = block_type_unordered_list
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_olist(self):
        markdown_text = """
            1. This is an olist
            2. Extra line
            3. one more line
            """
        r_out = block_type_ordered_list
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_wrong_olist(self):
        markdown_text = """
            1. This is an olist
            3. This is not :(
            """
        r_out = block_type_paragraph
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_wrong_olist2(self):
        markdown_text = """
            1. This is an olist
            This is not
            """
        r_out = block_type_paragraph
        markdown_type = block_to_block_type(markdown_text)
        self.assertEqual(markdown_type, r_out)

    def test_html(self):
        markdown_test = """
            # This is a header

            ## This is also a header

            ###### This is a third header

            1. This is the start of an ordered list
            2. This is an ordrered list too

            * This is an unordered list
            * Also unordered

            1. This is a fake list
            Should be a paragraph

            This will also be a paragraph
            Continue with a paragraph

            ```
            This is a code
            More code
            I hope code works well
            ```

            ```
            This is fake code
            Should be a paragraph

            - This is an unordered list
            Fake tho, paragraph whatttt
            """
        r_out = "<div><h1>This is a header</h1><h2>This is also a header</h2><h6>This is a third header</h6><ol><li>This is the start of an ordered list</li><li>This is an ordrered list too</li></ol><ul><li>This is an unordered list</li><li>Also unordered</li></ul><p>1. This is a fake list\nShould be a paragraph</p><p>This will also be a paragraph\nContinue with a paragraph</p><pre><code>This is a code\nMore code\nI hope code works well</code></pre><p>```\nThis is fake code\nShould be a paragraph</p><p>- This is an unordered list\nFake tho, paragraph whatttt</p></div>"
        html_test = markdown_to_html_node(markdown_test)
        self.assertEqual(html_test, r_out)

if __name__=="__main__":
    unittest.main()
