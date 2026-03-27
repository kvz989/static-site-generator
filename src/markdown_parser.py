import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            title = block[2:].strip()
            return title
    raise Exception("Title not found")


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = [item.strip() for item in blocks]
    cleaned_blocks = [item for item in stripped_blocks if item]
    return cleaned_blocks


def block_to_block_type(markdown_block):
    if markdown_block == "":
        return
    match_heading = re.match(r"^(#{1,6})\s+(.*)", markdown_block)
    if match_heading:
        return BlockType.HEADING
    if len(markdown_block) >= 7:
        first_four_characters = markdown_block[:4]
        last_three_characters = markdown_block[-3:]
        if first_four_characters == "```\n" and last_three_characters == "```":
            return BlockType.CODE
    if markdown_block[0] == ">":
        return BlockType.QUOTE
    if len(markdown_block) >= 2:
        if markdown_block[:2] == "- ":
            return BlockType.UNORDERED_LIST
    match_number = re.match(r"^(\d+)\.", markdown_block)
    is_ordered_list = False
    if match_number:
        lines = markdown_block.split("\n")
        for i, line in enumerate(lines, start=1):
            is_ordered_list = False
            match_ordered_list = re.match(r"^(\d+)\. (.+)", line)
            if match_ordered_list and int(match_ordered_list.group(1)) == i:
                is_ordered_list = True
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_type_to_html_node(block, block_type)
        children.append(block_node)
    return ParentNode("div", children)


def block_type_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(line.strip() for line in lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            new_lines.append(line[2:])
        else:
            new_lines.append(line[1:])
    text = " ".join(line.strip() for line in new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line.split(". ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
