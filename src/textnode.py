from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    PLAIN_TEXT = "plaintext"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(node):
    if node.text_type not in TextType:
        raise ValueError("Text type invalid")
    match node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode(tag="i", value=node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=node.text, props={"href": node.url})
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": node.url, "alt": node.text},
            )
