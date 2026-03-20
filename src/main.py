from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


def main():
    # test_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(test_node)
    # leaf_node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
    # print(leaf_node)

    node = ParentNode(
        "p",
        [
            LeafNode("b", "bold"),
            LeafNode(None, "plaintext"),
            LeafNode("i", "italic"),
            LeafNode(None, "plaintext"),
        ],
    )
    print(node.to_html())


if __name__ == "__main__":
    main()
