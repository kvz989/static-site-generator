import os
import shutil
from pathlib import Path

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import extract_title, markdown_to_html_node
from textnode import TextNode, TextType


def main():

    update_public()
    input_path = "content/index.md"
    template_path = "template.html"
    output_path = "public/index.html"
    generate_page(input_path, template_path, output_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = Path(from_path).read_text()
    template = Path(template_path).read_text()
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()
    title = extract_title(md)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", content)
    Path(dest_path).write_text(result)


def update_public():
    static_dir = "static"
    public_dir = "public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    static_path = Path(static_dir)
    public_path = Path(public_dir)
    copy_static(static_path, public_path)


def copy_static(src, dst):
    dst.mkdir(mode=0o755)
    for entry in src.iterdir():
        if entry.is_file():
            shutil.copy(entry, dst / entry.name)
        else:
            copy_static(entry, dst / entry.name)


if __name__ == "__main__":
    main()
