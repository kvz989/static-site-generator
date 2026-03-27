import unittest

from markdown_parser import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("This is a text node", TextType.PLAIN_TEXT, "url")
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT, "url")
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.props["href"], "https://www.google.com")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]

    def test_image(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, "https://www.google.com/example.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.props["src"], "https://www.google.com/example.jpg")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]
        self.assertEqual(html_node.props["alt"], "This is an image")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]

    def test_markdown_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], test_nodes[i])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with two links - one: [click me!](https://www.google.com) and two: [click me, too!](https://www.yahoo.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with two links - one: ", TextType.PLAIN_TEXT),
                TextNode("click me!", TextType.LINK, "https://www.google.com"),
                TextNode(" and two: ", TextType.PLAIN_TEXT),
                TextNode("click me, too!", TextType.LINK, "https://www.yahoo.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        test_string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(test_string)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

        # print("split_nodes_delimiter called")
        # new_nodes = text_to_textnodes(test_string)
        # for node in new_nodes:
        #     print(node)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        md = "test"
        block_type1 = block_to_block_type(md)
        block_type2 = BlockType.PARAGRAPH
        self.assertEqual(block_type1, block_type2)

    def test_block_to_block_type_heading(self):
        mds = (
            "# test",
            "## test",
            "### test",
            "#### test",
            "##### test",
            "###### test",
        )
        bad_mds = ("#test", "test")
        for md in mds:
            block_type = block_to_block_type(md)
            self.assertEqual(block_type, BlockType.HEADING)
        for bad_md in bad_mds:
            block_type = block_to_block_type(bad_md)
            self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```\ntest```"
        block_type1 = block_to_block_type(md)
        block_type2 = BlockType.CODE
        self.assertEqual(block_type1, block_type2)

    def test_block_to_block_type_quote(self):
        md = ">test"
        block_type1 = block_to_block_type(md)
        block_type2 = BlockType.QUOTE
        self.assertEqual(block_type1, block_type2)

    def test_block_to_block_type_unordered_list(self):
        md = "- test"
        block_type1 = block_to_block_type(md)
        block_type2 = BlockType.UNORDERED_LIST
        self.assertEqual(block_type1, block_type2)

    def test_block_to_block_type_ordered_list(self):
        mds = ["1. test\n2. test\n3. test", "1. test"]
        bad_mds = ["1.test", "test", "1. test\n3. test"]
        # for md in mds:
        # block_type = block_to_block_type(md)
        # self.assertEqual(block_type, BlockType.ORDERED_LIST)
        for bad_md in bad_mds:
            block_type = block_to_block_type(bad_md)
            self.assertNotEqual(block_type, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
