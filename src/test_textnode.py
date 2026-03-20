import unittest

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
        node = TextNode("This is a text node", "bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_italic(self):
        node = TextNode("This is a text node", "italic")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_code(self):
        node = TextNode("This is a text node", "code")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]

    def test_link(self):
        node = TextNode("This is a text node", "link", "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.value, "This is a text node")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.props["href"], "https://www.google.com")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]

    def test_image(self):
        node = TextNode(
            "This is an image", "image", "https://www.google.com/example.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")  # pyright: ignore[reportOptionalMemberAccess]
        self.assertEqual(html_node.props["src"], "https://www.google.com/example.jpg")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]
        self.assertEqual(html_node.props["alt"], "This is an image")  # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]


if __name__ == "__main__":
    unittest.main()
