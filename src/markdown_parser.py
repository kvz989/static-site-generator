import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    original_text_node = TextNode(text, TextType.PLAIN_TEXT)
    bold_nodes = split_nodes_delimiter([original_text_node], "**", TextType.BOLD_TEXT)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC_TEXT)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # print(f"delimiter: {delimiter}, text_type: {text_type}")
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception(
                    "Invalid Markdown syntax. Incorrect number of delimiters."
                )
            for i in range(len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_node = TextNode(split_nodes[i], TextType.PLAIN_TEXT)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_nodes[i], text_type)
                    # print(f"created node: {new_node}")
                    new_nodes.append(new_node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        image_matches = extract_markdown_images(node.text)
        original_text = node.text
        if not image_matches:
            remainder_node = TextNode(node.text, TextType.PLAIN_TEXT)
            new_nodes.append(remainder_node)
            continue
        for match in image_matches:
            split_nodes = original_text.split(f"![{match[0]}]({match[1]})", 1)
            text_before_node = TextNode(split_nodes[0], TextType.PLAIN_TEXT)
            text_after_node = TextNode(match[0], TextType.IMAGE, match[1])
            if split_nodes[0] != "":
                new_nodes.append(text_before_node)
            new_nodes.append(text_after_node)
            original_text = split_nodes[1]
        if original_text != "":
            remainder_node = TextNode(original_text, TextType.PLAIN_TEXT)
            new_nodes.append(remainder_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        link_matches = extract_markdown_links(node.text)
        original_text = node.text
        if not link_matches:
            remainder_node = TextNode(node.text, TextType.PLAIN_TEXT)
            new_nodes.append(remainder_node)
            continue
        for match in link_matches:
            split_nodes = original_text.split(f"[{match[0]}]({match[1]})", 1)
            text_before_node = TextNode(split_nodes[0], TextType.PLAIN_TEXT)
            text_after_node = TextNode(match[0], TextType.LINK, match[1])
            if split_nodes[0] != "":
                new_nodes.append(text_before_node)
            new_nodes.append(text_after_node)
            original_text = split_nodes[1]
        if original_text != "":
            remainder_node = TextNode(original_text, TextType.PLAIN_TEXT)
            new_nodes.append(remainder_node)
    return new_nodes


def extract_markdown_images(text):
    image_re = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(rf"{image_re}", text)
    return matches


def extract_markdown_links(text):
    link_re = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(rf"{link_re}", text)
    return matches
